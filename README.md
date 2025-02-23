## Inspiration

Our campus research reveals that UW-Madison students face two distinct challenges: the lack of a dedicated online university community for meaningful connections, and difficulty discovering Madison's social activities. Our platform transforms the Madison college experience by making it easier to find both exciting local adventures and meaningful campus connections.

## What it does

MadLuv offers a specialized matchmaking and activity recommendation service for university students. Users authenticate with their university email, ensuring a secure, campus-focused community. Through our assessment questionnaire, students create profiles that capture their characteristics and interests. 

Our matching algorithm then identifies and suggests compatible connections based on shared interests and complementary traits. When mutual interest exists, students can initiate contact through the platform. To enhance these new connections, we provide recommendations for activities that are ideal for meetups, specifically selected to match the interests and preferences of both people.

## How we built it

Our platform is built on two core algorithms: a partner matching system and an activity recommendation engine. The matching system used a [speed dating dataset](https://www.kaggle.com/datasets/ulrikthygepedersen/speed-dating/data) from Kaggle to pre-train our gradient boosting model, which predicts compatibility scores between users. We developed a data pipeline that processes user inputs through our local database to match the model's required format. The activity recommendation system combines web-scraped campus resources with user characteristics to generate personalized suggestions. The system is implemented through a Streamlit interface foruser interaction.

## Challenges we ran into

The most significant technical challenge is implementing the partner matching system, due to the unique structure of our dataset, where each record represents a pairing of two individuals rather than a single user profile. This required us to design a sophisticated data pipeline for proper format conversion and processing. What's more, despite coming from diverse international backgrounds and working across language barriers, our team successfully collaborated to overcome these technical complexities.

## Accomplishments that we're proud of

We developed a comprehensive platform from the ground up, designing and implementing its entire architecture with two unique features. Our application addresses two crucial needs simultaneously: enhancing students' social connections and helping them discover Madison's social landscape. It serves as an invaluable resource for both current students looking to enrich their social lives and newcomers seeking to navigate their Madison journey.

## What we learned

In the current AI era, we realized that creating effective solutions for meaningful societal challenges is vital. Our project began with a lot of  research to identify truly valuable problems worth solving. We then used the help of  modern technologies to develop efficient solutions. This project is our team's first experience into building a comprehensive full-stack application with integrated machine learning systems. Through this process, we gained invaluable experience in workflow management and end-to-end application development.

## What's next for MadLuv

As UW-Madison students, we are deeply committed to enhancing our campus community. After launch, we plan to leverage user data to continuously refine our recommendation model, making it even more effective at creating meaningful connections. Security remains a vital priority - we will implement robust protection measures and advanced detection systems for malicious behavior. We want to provide fellow Badgers with a secure, trustworthy platform they can enhance their social life in madison.
