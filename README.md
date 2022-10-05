# IMAGE CLASSIFIER WEB APP

This web application provides classification service for any image to 10 different classes such as airplanes, cars, birds, cats, deer, dogs, frogs, horses, ships, and trucks using CNN model trained with [CIFAR-10](https://www.kaggle.com/c/cifar-10).

### Model
The model is created using [Xception](https://keras.io/api/applications/xception/) convolutional base and can be changed to users model via website form.
Such methods as data augmentation, DropBlock2D, GlobalAveragePooling2D, Dropblock, ReduceLROnPlateau are used to prevent an overfitting of the model.
The model's test accuracy score is 97.16% on [CIFAR-10](https://www.kaggle.com/c/cifar-10) test dataset.

### Installation
1. You need to have pre installed IDE and Docker
2. Create new project and clone project from git in your IDE
3. Create .env file in project root and fill in the file like this example:<br />
DB_NAME=ImageClassifier<br />
DB_USER=postgres<br />
DB_PASS=password<br />
DB_HOST=db<br />
DB_PORT=5432<br />
ALLOWED_HOSTS=*<br />
SECRET_KEY=testkey<br />
4. Open in terminal project root where docker-compose.yml and paste this command: docker-compose build.
5. Wait when docker-compose build will be finished and paste next command: docker-compose up.
6. Now you can see that project is running and it is appear in docker application where u can start/stop server in future.
7. And you can go in your browser in path: 127.0.0.1:8000 and use classifier. <br />
Here is Video Example with all this steps to run this project: <br />
https://youtu.be/C29xnfGF3II
