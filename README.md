# Goliath National Bank - Core Banking Application 

We Built This Bank For You. Changing lives; one member at a time!

*  Implemented Core Banking Application using Python Flask Framework with virtually any size with horizontal scaling DynamoDB as Data Base.
*  Deployed Application to AWS in an Auto scaled EC2 Cluster with Load Balancer

## Application Demo: [YouTube Link](https://youtu.be/v-OQK1FqT6A) 

## Group Members:

   ###### [PREETI PARIHAR](https://www.linkedin.com/in/preetiparihar/)
   ###### [ANANTH UPADHYA](https://www.linkedin.com/in/560085/)
   ###### [DEESHA DESAI](https://www.linkedin.com/in/deeshadesai/)
   ###### [PRIYANKA DEVENDRAN](https://www.linkedin.com/in/priyanka-devendran-76244479/)

## [Project Journal](https://github.com/gopinathsjsu/team-project-the-elite/tree/master/Documents/Journal)

## [Google Sprint Task Sheet](https://github.com/gopinathsjsu/team-project-the-elite/blob/master/Documents/Sprint%20Task%20Sheet_Four%20Real-1%20(3)%20(1).xlsx)

## [Burn Down Chart](https://github.com/gopinathsjsu/team-project-the-elite/blob/master/Documents/Burn_Down.png)

## XP Core Values Implemented:

*  Ananth Upadhya - Communication <br/>
         Communication between team members helped in sharing of knowledge, clarifying issues, understanding blockers and resolving them.
	 
*  Preeti Parihar - Courage <br/>
	Courage helped in taking tasks which we new and helped in challenging ourselves on the technologies which were new. For me microservice deployment is completely new concept. I could have deploy a single monolith but monolith doesn't scale well specially when we need horizontal scaling. But I took this challenge and decided to deploy our solution as microservice deployment. I faced another challenge of learning Docker. Docker is completely new concept for me but I learnt it and deploy my services with it. Also configuring Nginx was also challenging. I faced issue regarding CORS after deployment.
	
*  Deesha Desai - Simplicity <br/>
	Simplicity helped in keeping the application design simple and to the point. It also helped in identifying easier ways to address the requirements.
	
*  Priyanka Devendran - Feedback <br/>
	Feedback helped in continuous improvement and knowing where one is going wrong and what can be done to improve

## Architecture Diagram

![](Images/Banking.png)


## Deployment Diagram

![](Images/Deployment_Diagram.png)

## Use Case Diagram

![](Images/UsecaseDiagram.png)

## [Project Board](https://trello.com/b/acPKH3pw)

Sprint Board
![](ProjectBoard/SprintBoard.PNG)

Sprint Backlog
![](ProjectBoard/SprintBacklog.PNG)

Sprint Inprogress
![](ProjectBoard/SprintInProgress.PNG)
![](ProjectBoard/SprintInProgress1.PNG)

Sprint InReview
![](ProjectBoard/SprintInReview.PNG)

Sprint Complete
![](ProjectBoard/TestedComplete.PNG)
![](ProjectBoard/SprintComplete.PNG)

## Design Pattern

We have used MVC architecture.

![](MVC.jpg)


## AWS AutoScaling

Elastic Load Balancer
![](Images/elb.png)

Target Group
![](Images/Target_group.png)

Amazon Machine Image
![](Images/ami.png)

Auto Scaling Group Details and Launch Configuration
![](Images/Launch_conf.png)

Scaling Policies
![](Images/Scaling_policy.png)

AB Testing
![](Images/ab-testing.png)

Scaled Instances
![](Images/scaled-instances.png)



## Application Setup 

### Step 1 : store following key, values in env.list
```
COGNITO_USER_POOL_ID=<value>
COGNITO_APP_CLIENT_ID=<value>
AWS_ACCESS_KEY_ID=<value>
AWS_SECRET_ACCESS_KEY=<value>
AWS_REGION=<value>
```

### Step 2: Install and setup Nginx

```
https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04
```

Replace following with ```/etc/nginx/sites-available/default```


```
upstream ui {
    server localhost:81;
}

upstream backend {
    server localhost:82;
}

server {
	listen 80 default_server;
	listen [::]:80 default_server;

	root /var/www/html;

	# Add index.php to the list if you are using PHP
	index index.html index.htm index.nginx-debian.html;

	server_name localhost;

   location / {
      # First attempt to serve request as file, then
      # as directory, then fall back to displaying a 404.
      proxy_set_header Host $host;
      #proxy_cookie_domain localhost;
      proxy_pass http://ui;
      #try_files $uri $uri/ =404;
   }

	location = /app {
	    return 302 /app/;
	}

      location /app {
         proxy_set_header Host $host;
         proxy_pass http://backend/;
      }
}
```

```
sudo nginx -t
sudo systemctl restart nginx
```

### Step 3: Install and setup Docker
```
sudo apt-get update
sudo apt install docker.io
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker 
docker ps
```

### Step 4: Run Goliath Banking services

#### Frontend
```
docker run -it -d -p 81:80 --name gnb_ui preetiparihar/gnb-ui:latest

docker logs gnb_ui:latest

```

#### Backend

```
docker run -it -d -p 82:8000 --env-file env.list --name gnb_app preetiparihar/gnb-app:latest

docker logs gnb_app:latest
```

### Step3: Test APIs
Use postman to test apis.
Import postman collection and environments


## Website Screenshots

#### Login
![](WebsiteScreenshots/login.png)
#### Register
![](WebsiteScreenshots/register.png)
#### User Home page

![](WebsiteScreenshots/userDashboard1.png) 
![](WebsiteScreenshots/userDashboard2.png)
#### User Accounts 

![](WebsiteScreenshots/myAccounts.png)
#### Deposit

![](WebsiteScreenshots/deposit.png)
#### Withdrawal

![](WebsiteScreenshots/withdrawal.png)
#### Transfer(OneTime & Recurring)

![](WebsiteScreenshots/Transfer.png)
![](WebsiteScreenshots/externalInternal.png)
![](WebsiteScreenshots/onetime.png)
![](WebsiteScreenshots/recurring.png)
#### Add Account
![](WebsiteScreenshots/userAddAccount.png)

#### Delete Account
![](WebsiteScreenshots/deleteAccount.png)
#### Admin home page
![](WebsiteScreenshots/adminDashboard.png)
#### Admin Transactions
![](WebsiteScreenshots/adminTransactions.png)
#### Refund
![](WebsiteScreenshots/refund.png)
#### Charge Fees
![](WebsiteScreenshots/chargeFees.png)
#### Add Account by Admin

![](WebsiteScreenshots/adminAddAccount.png)

