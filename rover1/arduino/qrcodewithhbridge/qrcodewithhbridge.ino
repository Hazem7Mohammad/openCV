//original code
#include <ros.h>
#include <std_msgs/Int16.h>
#include <geometry_msgs/Pose2D.h>
#define EN_L 3
#define IN1_L 8
#define IN2_L 7
#define EN_R 9
#define IN1_R 5
#define IN2_R 4

ros::NodeHandle
nh;
float x = 0.0;
float y = 0.0;
float area =0.0;


int speed = 160;//Change the speed of the car


//Left and Right values
int lowval=200;//To turn right
int highval=440;//To turn left


//------------------Call Backs-----------------------------
void callback( const geometry_msgs::Pose2D& pose_message){
  nh.loginfo("Received a message");
if((y==0)&&(x==0)){
     analogWrite(EN_R, speed);
     digitalWrite(IN1_R, LOW);
     digitalWrite(IN2_R, LOW);
     analogWrite(EN_L, speed);
     digitalWrite(IN1_L, LOW);
     digitalWrite(IN2_L, LOW);
  // saving the messages in x & y variables
  
}
  x = pose_message.x;
  y = pose_message.y;
  area = pose_message.theta;
// if the target in the middle stop
if ((lowval<x && x<highval)){
  nh.loginfo("Stop");
     analogWrite(EN_R, speed);
     digitalWrite(IN1_R, LOW);
     digitalWrite(IN2_R, LOW);
     analogWrite(EN_L, speed);
     digitalWrite(IN1_L, LOW);
     digitalWrite(IN2_L, LOW);
}
//Target on the right
else if(x<lowval){
  nh.loginfo("Going right");
go_right();
}
//target on the left
else{
  nh.loginfo("Going left");
go_left();
}
}
//---------------------------------------------------------
ros::Subscriber<geometry_msgs::Pose2D> servo_n("pose", &callback );
/* create a subscriber node named servo_n that
* receive the msg (type Pose2D) from the topic
x_pose then invoke the callback
*/
//----------------------------------------------------
void setup()
{
 nh.initNode();
 nh.subscribe(servo_n);
//set the subscriber named servo_n to subscribe

  Serial.begin(9600);
  pinMode(EN_L, OUTPUT);
  pinMode(EN_R, OUTPUT);
  pinMode(IN1_L, OUTPUT);
  pinMode(IN2_L, OUTPUT);
  pinMode(IN1_R, OUTPUT);
  pinMode(IN2_R, OUTPUT);
  digitalWrite(EN_L, LOW);
  digitalWrite(EN_R, LOW);
  digitalWrite(IN1_L, LOW);
  digitalWrite(IN2_L, LOW);
  digitalWrite(IN1_R, LOW);
  digitalWrite(IN2_R, LOW);

}
void loop()
{
  nh.spinOnce();
  delay(300);
}


void go_left (){
     analogWrite(EN_L, speed);
     digitalWrite(IN1_L, HIGH);
     digitalWrite(IN2_L, LOW);
     analogWrite(EN_R, speed);
     digitalWrite(IN1_R, HIGH);
     digitalWrite(IN2_R, LOW);
     delay(50);
    digitalWrite(EN_L, LOW);
    digitalWrite(EN_R, LOW);
    digitalWrite(IN1_L, LOW);
    digitalWrite(IN2_L, LOW);
    digitalWrite(IN1_R, LOW);
    digitalWrite(IN2_R, LOW);
return ;
}

void go_right (){
     analogWrite(EN_L, speed);
     digitalWrite(IN1_L, LOW);
     digitalWrite(IN2_L, HIGH);
     analogWrite(EN_R, speed);
     digitalWrite(IN1_R, LOW);
     digitalWrite(IN2_R, HIGH);
delay(50);
    digitalWrite(EN_L, LOW);
    digitalWrite(EN_R, LOW);
    digitalWrite(IN1_L, LOW);
    digitalWrite(IN2_L, LOW);
    digitalWrite(IN1_R, LOW);
    digitalWrite(IN2_R, LOW);
     
return ;
}
