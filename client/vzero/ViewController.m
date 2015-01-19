//
//  ViewController.m
//  vzero
//
//  Created by Alberto López on 19/01/15.
//  Copyright (c) 2014 Commerce Factory. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    [self.indicatorWaitingForSubscription stopAnimating];
    self.manager = [AFHTTPRequestOperationManager manager];
    [self getPlansFromBraintreeMerchantAccount];
    [self getClientToken];
}

- (void)getClientToken {

    [self.manager GET:@"http://127.0.0.1:8000/getClientToken"
          parameters: nil
          success: ^(AFHTTPRequestOperation *operation, id responseObject) {
            self.clientToken = responseObject[@"clientToken"];
            self.startSubscriptionButton.enabled = TRUE;
          }
          failure:^(AFHTTPRequestOperation *operation, NSError *error) {
            NSLog(@"Error: %@", error);
          }];
}

- (IBAction)startSubscription:(id)sender {
    Braintree *braintree = [Braintree braintreeWithClientToken:self.clientToken];
    BTDropInViewController *dropInViewController = [braintree dropInViewControllerWithDelegate:self];
    
    dropInViewController.navigationItem.leftBarButtonItem = [[UIBarButtonItem alloc]
                                                             initWithBarButtonSystemItem:UIBarButtonSystemItemCancel
                                                             target:self
                                                             action:@selector(userDidCancelPayment)];
    
    //Customize the UI
    dropInViewController.summaryTitle = @"Creating Subscription";
    dropInViewController.summaryDescription = self.selectedPlan;
    
    UINavigationController *navigationController = [[UINavigationController alloc]
                                                    initWithRootViewController:dropInViewController];
    [self presentViewController:navigationController
                       animated:YES
                     completion:nil];

}

- (void)dropInViewController:(__unused BTDropInViewController *)viewController didSucceedWithPaymentMethod:(BTPaymentMethod *)paymentMethod {
    [self postNonceToServer:paymentMethod.nonce];
    [self dismissViewControllerAnimated:YES completion:nil];
}

- (void)dropInViewControllerDidCancel:(__unused BTDropInViewController *)viewController {
    [self dismissViewControllerAnimated:YES completion:nil];
}

-(void) userDidCancelPayment{
    [self dismissViewControllerAnimated:YES completion:nil];
}

#pragma mark delegate methods for UIPickerView

// The number of rows of data
-(NSInteger)pickerView:(UIPickerView *)pickerView numberOfRowsInComponent:(NSInteger)component
{
    return self.billPlans.count;
}

// The data to return for the row and component (column) that's being passed in
- (NSString*)pickerView:(UIPickerView *)pickerView titleForRow:(NSInteger)row forComponent:(NSInteger)component
{
    return self.billPlans[row];
}

// The number of columns of data
- (NSInteger)numberOfComponentsInPickerView:
(UIPickerView *)pickerView
{
    return 1;
}

// Catpure the picker view selection
- (void)pickerView:(UIPickerView *)pickerView didSelectRow:(NSInteger)row inComponent:(NSInteger)component
{
    self.selectedPlan = self.billPlans[row];
}

-(void) getPlansFromBraintreeMerchantAccount{
    
    [self.manager GET:@"http://127.0.0.1:8000/getBillPlans"
           parameters: nil
              success: ^(AFHTTPRequestOperation *operation, id responseObject) {
                  self.billPlans = responseObject[@"planIDs"];
                  
                  // Connect data
                  self.selectedPlan = self.billPlans[0];
                  self.pickerViewTypeOfSubscription.dataSource = self;
                  self.pickerViewTypeOfSubscription.delegate = self;
                  
              }
              failure:^(AFHTTPRequestOperation *operation, NSError *error) {
                  NSLog(@"Error: %@", error);
              }];
}



#pragma mark POST NONCE TO SERVER method
- (void)postNonceToServer:(NSString *)paymentMethodNonce {
    
    [self.indicatorWaitingForSubscription startAnimating];
    
    [self.manager POST:@"http://127.0.0.1:8000/createSubscription"
       parameters:@{@"payment_method_nonce": paymentMethodNonce,
                    @"plan_id": self.selectedPlan,
                    }
          success:^(AFHTTPRequestOperation *operation, id responseObject) {
              NSString *subscriptionIDText = responseObject[@"subscription_id"];
              
              [self.indicatorWaitingForSubscription stopAnimating];

              self.subscriptionID.text = [NSString stringWithFormat:@"Subscription ID: %@", subscriptionIDText];
              
              
          }
          failure:^(AFHTTPRequestOperation *operation, NSError *error) {
              NSLog(@"Error: %@", error);
          }];
    
}

@end
