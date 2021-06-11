This is AddTask Python Microservice

It has the dockerfile which is used to create image to be used in 

containerDefinition part of ECS TaskDefinition

This is a frontend facing microservice with which end users communicate 

Therefore it is hosted on an ECS Container EC2 Instance inside an ECS cluster residing in a public subnet

behind a public ALB , This microservice communicates with the backend dbtask microservice via private ALB to insert new records in the SQLITE database
