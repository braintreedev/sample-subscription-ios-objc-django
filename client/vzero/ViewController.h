//
//  ViewController.h
//  vzero
//
//  Created by Alberto López on 19/01/15.
//  Copyright (c) 2014 Commerce Factory. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "AFNetworking.h"
#import "Braintree/Braintree.h"

@interface ViewController : UIViewController<BTDropInViewControllerDelegate,UIPickerViewDataSource, UIPickerViewDelegate>

@property (strong, nonatomic) NSString *clientToken;
@property (strong, nonatomic) AFHTTPRequestOperationManager *manager;
@property (strong, nonatomic) IBOutlet UIButton *startSubscriptionButton;
@property (weak, nonatomic) IBOutlet UIPickerView *pickerViewTypeOfSubscription;
@property (strong, nonatomic) NSArray *billPlans;
@property (strong, nonatomic) NSString *selectedPlan;
@property (strong, nonatomic) IBOutlet UILabel *subscriptionID;
@property (strong, nonatomic) IBOutlet UIActivityIndicatorView *indicatorWaitingForSubscription;


- (IBAction)startSubscription:(id)sender;

@end
