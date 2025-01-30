## Amz && Movie User Thinking
#####################dataset construction#####################
#### amz
"""You are an expert recommender engine. Your task is to determine if the user will like the target book.

We will provide you with the following information:
- The user's historical interactions in the format [Book NAME, RATING], where a RATING greater than 4 indicates a like, and a RATING of 4 or less indicates a dislike.
- The target book's name.

<User History>{}</User History>

<Target Book Name>{}</Target Book Name>

Please strictly follow the following format:
<User Preference>[Summarize user preference on books in 200 words. Do not include any information about target book please. You should think step by step.]</User Preference>
<Final Verdict>["user will like the target book" or "user will not like the target book" here]</Final Verdict>
"""

##################### fine-tune #####################
#### amz
"""You are an expert recommender engine. Your task is to inference the user preference.

We will provide you with the following information:
- The user's historical interactions in the format [Book NAME, RATING], where a RATING greater than 4 indicates a like, and a RATING of 4 or less indicates a dislike.

<User History>{}</User History>

Summarize user preference on books in 200 words. You should think step by step."""

#####################dataset construction#####################
#### movie
"""You are an expert recommender engine. Your task is to determine if the user will like the target movie.

We will provide you with the following information:
- The user's historical interactions in the format [MOVIE NAME (YEAR), RATING], where a RATING greater than 3 indicates a like, and a RATING of 3 or less indicates a dislike. 
- The target movie's name.

<User History>{}</User History>

<Target Movie Name>{}</Target Movie Name>

Please strictly follow the following format:
<User Preference>[Summarize user preference on movies in 200 words. Do not include any information about target movie please. You should think step by step.]</User Preference>
<Final Verdict>["user will like the target movie" or "user will not like the target movie" here]</Final Verdict>
"""

##################### fine-tune #####################
#### movie
"""You are an expert recommender engine. Your task is to inference the user preference.

We will provide you with the following information:
- The user's historical interactions in the format [MOVIE NAME (YEAR), RATING], where a RATING greater than 3 indicates a like, and a RATING of 3 or less indicates a dislike.

<User History>{}</User History>

Summarize user preference on movies in 200 words. You should think step by step."""

## Amz && Movie Item Thinking
#####################dataset construction#####################
#### amz
"""You are an expert recommender engine. Your task is to determine if the target user will like the target book.

We will provide you with the following information:
- The target book's name.
- The historical interactions of one user who likes the target book and one user who does not. The historical interactions are in the format [Book NAME, RATING], where a RATING greater than 4 indicates a like, and a RATING of 4 or less indicates a dislike.
- The historical interactions of the target user.

<Target Book Name>{}</Target Book Name>

<Like User History>{}</Like User History>

<Dislike User History>{}</Dislike User History>

<Target User History>{}</Target User History>

Please strictly follow the following format:
<Book Knowledge>[Summarize your knowledge about the target book in 200 words. Include the following: 1. The book's basic attributes, such as genre, author, writing style, theme, and setting. 2. The characteristics of users who like the target book. 3. The characteristics of users who dislike the target book. Do not include any information about the target user. You should think step by step.]</Book Knowledge>
<Final Verdict>["target user will like the target book" or "target user will not like the target book" here]</Final Verdict>
"""

##################### fine-tune #####################
#### amz
"""You are an expert recommender engine. Your task is to inference knowledge about the target book.

We will provide you with the following information:
- The target book's name.
- The historical interactions of one user who likes the target book and one user who does not. The historical interactions are in the format [Book NAME, RATING], where a RATING greater than 4 indicates a like, and a RATING of 4 or less indicates a dislike.

<Target Book Name>{}</Target Book Name>

<Like User History>{}</Like User History>

<Dislike User History>{}</Dislike User History>

Summarize your knowledge about the target book in 200 words. Include the following: 1. The book's basic attributes, such as genre, author, writing style, theme, and setting. 2. The characteristics of users who like the target book. 3. The characteristics of users who dislike the target book. You should think step by step."""

#####################dataset construction#####################
#### movie
"""You are an expert recommender engine. Your task is to determine if the target user will like the target movie.

We will provide you with the following information:
- The target movie's name.
- The historical interactions of one user who likes the target movie and one user who does not. The historical interactions are in the format [MOVIE NAME (YEAR), RATING], where a RATING greater than 3 indicates a like, and a RATING of 3 or less indicates a dislike.
- The historical interactions of the target user.

<Target Movie Name>{}</Target Movie Name>

<Like User History>{}</Like User History>

<Dislike User History>{}</Dislike User History>

<Target User History>{}</Target User History>

Please strictly follow the following format:
<Movie Knowledge>[Summarize your knowledge about the target movie in 200 words. Include the following: 1.The target movie's basic attributes, such as genre, director/cast, country, character, plot/theme, mood/tone, critical acclaim/award. 2.The characteristics of users who like the movie. 3. The characteristics of users who dislike the movie. Do not include any information about the target user. You should think step by step.]</Movie Knowledge>
<Final Verdict>["target user will like the target movie" or "target user will not like the target movie" here]</Final Verdict>
"""

##################### fine-tune #####################
#### movie
"""You are an expert recommender engine. Your task is to inference knowledge about the target movie.

We will provide you with the following information:
- The target movie's name.
- The historical interactions of one user who likes the target movie and one user who does not. The historical interactions are in the format [MOVIE NAME (YEAR), RATING], where a RATING greater than 3 indicates a like, and a RATING of 3 or less indicates a dislike.

<Target Movie Name>{}</Target Movie Name>

<Like User History>{}</Like User History>

<Dislike User History>{}</Dislike User History>

Summarize your knowledge about the target movie in 200 words. Include the following: 1.The target movie's basic attributes, such as genre, director/cast, country, character, plot/theme, mood/tone, critical acclaim/award. 2.The characteristics of users who like the movie. 3. The characteristics of users who dislike the movie. You should think step by step."""


## Amz && Movie User Reflecting
#####################dataset construction#####################
### amz
"""Please act as an impartial judge. Below is a user's question and your previous inferenced user preference. Evaluate the user preference and provide valuable reflection.

<Question>
We will provide you with the following information:
- The user's historical interactions in the format [Book NAME, RATING], where a RATING greater than 4 indicates a like, and a RATING of 4 or less indicates a dislike.
- The target book's name

<User History>{}</User History>

<Target Book Name>{}</Target Book Name>

Whether the user will like the target book?
</Question>

<Previous User Preference>{}</Previous User Preference>

There may be potential issues with the user preference analysis. Your task is to judge the correctness of the user preference and provide valuable reflection to the user preference. 
Please strictly follow the following format:
<Final Judgement>["The user preference is reasonable" or "The user preference is not reasonable"]</Final Judgement>
<Reflection>[If the user preference is not reasonable, you need provide variable reflection to the user preference. Identify key errors and potential misunderstanding here. (No more than 200 words).  Do not include any information about the target book please. If the user preference is reasonable, nothing here]</Reflection>
"""

##################### fine-tune #####################
"""Please act as an impartial judge. Below is a user's question and your previous inferenced user preference. Evaluate the correctness of the user preference and provide valuable reflection.

<Question>
We will provide you with the following information:
- The user's historical interactions in the format [Book NAME, RATING], where a RATING greater than 4 indicates a like, and a RATING of 4 or less indicates a dislike.

<User History>{}</User History>

Please inference the user preference.
</Question>

<Previous User Preference>{}</Previous User Preference>

There may be potential issues with the previous user preference analysis. Your task is to judge the correctness of the user preference and provide valuable reflection to the user preference. 
Please strictly follow the following format:
<Final Judgement>["The user preference is reasonable" or "The user preference is not reasonable"]</Final Judgement>
<Reflection>[If the user preference is not reasonable, you need to provide variable reflection to the user preference. Identify key errors and potential misunderstanding here. (No more than 200 words).  If the user preference is reasonable, nothing here]</Reflection>"""


#####################dataset construction#####################
### movie 
"""Please act as an impartial judge. Below is a user's question and your previous inferenced user preference. Evaluate the user preference and provide valuable reflection.

<Question>
We will provide you with the following information:
- The user's historical interactions in the format [MOVIE NAME (YEAR), RATING], where a RATING greater than 3 indicates a like, and a RATING of 3 or less indicates a dislike. 
- The target movie's name.

<User History>{}</User History>

<Target Movie Name>{}</Target Movie Name>

Whether the user will like the target movie?
</Question>

<Previous User Preference>{}</Previous User Preference>

There may be potential issues with the user preference analysis. Your task is to judge the correctness of the user preference and provide valuable reflection to the user preference. 
Please strictly follow the following format:
<Final Judgement>["The user preference is reasonable" or "The user preference is not reasonable"]</Final Judgement>
<Reflection>[If the user preference is not reasonable, you need provide variable reflection to the user preference. Identify key errors and potential misunderstanding here. (No more than 200 words).  Do not include any information about the target movie please. If the user preference is reasonable, nothing here]</Reflection>
"""

##################### fine-tune #####################
"""Please act as an impartial judge. Below is a user's question and your previous inferenced user preference. Evaluate the correctness of the user preference and provide valuable reflection.

<Question>
We will provide you with the following information:
- The user's historical interactions in the format [MOVIE NAME (YEAR), RATING], where a RATING greater than 3 indicates a like, and a RATING of 3 or less indicates a dislike.

<User History>{}</User History>

Please inference the user preference.
</Question>

<Previous User Preference>{}</Previous User Preference>

There may be potential issues with the previous user preference analysis. Your task is to judge the correctness of the user preference and provide valuable reflection to the user preference. 
Please strictly follow the following format:
<Final Judgement>["The user preference is reasonable" or "The user preference is not reasonable"]</Final Judgement>
<Reflection>[If the user preference is not reasonable, you need to provide variable reflection to the user preference. Identify key errors and potential misunderstanding here. (No more than 200 words).  If the user preference is reasonable, nothing here]</Reflection>"""

## Amz && Movie Item Reflecting
#####################dataset construction#####################
### amz
"""Please act as an impartial judge. Below is a book knowledge inference question and your previous inferenced book knowledge. Evaluate the correctness of the book knowledge and provide valuable reflection.

<Question>
We will provide you with the following information:
- The target book's name.
- The historical interactions of one user who likes the book and one user who does not. The historical interactions are in the format [Book NAME, RATING], where a RATING greater than 4 indicates a like, and a RATING of 4 or less indicates a dislike.
- The historical interactions of the target user.

<Target Book Name>{}</Target Book Name>

<Like User History>{}</Like User History>

<Dislike User History>{}</Dislike User History>

<Target User History>{}</Target User History>

Whether the target user will like the target book?
</Question>

<Previous Book Knowledge>{}</Previous Book Knowledge>

There may be potential issues with the previous book knowledge analysis. Your task is to judge the correctness of the book knowledge and provide valuable reflection to the book knowledge. 
Please strictly follow the following format:
<Final Judgement>["The book knowledge is reasonable" or "The book knowledge is not reasonable"]</Final Judgement>
<Reflection>[If the book knowledge is not reasonable, you need to provide variable reflection to the book knowledge. Identify key errors and potential misunderstanding here. (No more than 200 words). Do not include any information about the target user. If the book knowledge is reasonable, nothing here]</Reflection>
"""

##################### fine-tune #####################
"""Please act as an impartial judge. Below is a book knowledge inference question and your previous inferenced book knowledge. Evaluate the correctness of the book knowledge and provide valuable reflection.

<Question>
We will provide you with the following information:
- The target book's name.
- The historical interactions of one user who likes the book and one user who does not. The historical interactions are in the format [Book NAME, RATING], where a RATING greater than 4 indicates a like, and a RATING of 4 or less indicates a dislike.

<Target Book Name>{}</Target Book Name>

<Like User History>{}</Like User History>

<Dislike User History>{}</Dislike User History>

Please inference knowledge about the target book.
</Question>

<Previous Book Knowledge>{}</Previous Book Knowledge>

There may be potential issues with the previous book knowledge analysis. Your task is to judge the correctness of the book knowledge and provide valuable reflection to the book knowledge. 
Please strictly follow the following format:
<Final Judgement>["The book knowledge is reasonable" or "The book knowledge is not reasonable"]</Final Judgement>
<Reflection>[If the book knowledge is not reasonable, you need to provide variable reflection to the book knowledge. Identify key errors and potential misunderstanding here. (No more than 200 words). If the book knowledge is reasonable, nothing here]</Reflection>"""


#####################dataset construction#####################
### movie
"""Please act as an impartial judge. Below is a movie knowledge inference question and your previous inferenced movie knowledge. Evaluate the correctness of the movie knowledge and provide valuable reflection.

<Question>
We will provide you with the following information:
- The target movie's name.
- The historical interactions of one user who likes the target movie and one user who does not. The historical interactions are in the format [MOVIE NAME (YEAR), RATING], where a RATING greater than 3 indicates a like, and a RATING of 3 or less indicates a dislike.
- The historical interactions of the target user.

<Target Movie Name>{}</Target Movie Name>

<Like User History>{}</Like User History>

<Dislike User History>{}</Dislike User History>

<Target User History>{}</Target User History>

Whether the target user will like the target movie?
</Question>

<Previous Movie Knowledge>{}</Previous Movie Knowledge>

There may be potential issues with the previous movie knowledge analysis. Your task is to judge the correctness of the movie knowledge and provide valuable reflection to the movie knowledge. 
Please strictly follow the following format:
<Final Judgement>["The movie knowledge is reasonable" or "The movie knowledge is not reasonable"]</Final Judgement>
<Reflection>[If the movie knowledge is not reasonable, you need to provide variable reflection to the movie knowledge. Identify key errors and potential misunderstanding here. (No more than 200 words). Do not include any information about the target user. If the movie knowledge is reasonable, nothing here]</Reflection>
"""

##################### fine-tune #####################
"""Please act as an impartial judge. Below is a movie knowledge inference question and your previous inferenced movie knowledge. Evaluate the correctness of the movie knowledge and provide valuable reflection.

<Question>
We will provide you with the following information:
- The target movie's name.
- The historical interactions of one user who likes the target movie and one user who does not. The historical interactions are in the format [MOVIE NAME (YEAR), RATING], where a RATING greater than 3 indicates a like, and a RATING of 3 or less indicates a dislike.

<Target Movie Name>{}</Target Movie Name>

<Like User History>{}</Like User History>

<Dislike User History>{}</Dislike User History>

Please inference knowledge about the target movie.
</Question>

<Previous Movie Knowledge>{}</Previous Movie Knowledge>

There may be potential issues with the previous movie knowledge analysis. Your task is to judge the correctness of the movie knowledge and provide valuable reflection to the movie knowledge. 
Please strictly follow the following format:
<Final Judgement>["The movie knowledge is reasonable" or "The movie knowledge is not reasonable"]</Final Judgement>
<Reflection>[If the movie knowledge is not reasonable, you need to provide variable reflection to the movie knowledge. Identify key errors and potential misunderstanding here. (No more than 200 words). If the movie knowledge is reasonable, nothing here]</Reflection>"""

## Amz && Movie User Refining
#####################dataset construction#####################
### amz

"""You are a helpful assistant for recommender system. Your task is to determine if the user will like the target book.

We will provide you with the following information:
- The user's historical interactions in the format [Book NAME, RATING], where a RATING greater than 4 indicates a like, and a RATING of 4 or less indicates a dislike.
- The target book's name.
- Your previous summarized user preference.
- Reflection on your previous summarized user preference.

<User History>{}</User  History>

<Target Book Name>{}</Target Book Name>

<Previous user preference>{}</Previous user preference>

<Reflection>{}</Reflection>

You should refine the previous user preference considering the reflection and give the final correct answer.

Please strictly follow the following format:
<Refined User Preference> [Summarize user preference here in 200 words. Do not include any information about the target book please. You should think step by step.] </Refined User Preference>
<Final Verdict> ["user will like the target book" or "user will not like the target book" here] </Final Verdict>
"""

##################### fine-tune #####################
### amz
"""You are an expert recommender engine. Your task is to inference the user preference.

We will provide you with the following information:
- The user's historical interactions in the format [Book NAME, RATING], where a RATING greater than 4 indicates a like, and a RATING of 4 or less indicates a dislike.
- Your previous summarized user preference.
- Reflection on your previous summarized user preference.

<User History>{}</User History>

<Previous User Preference>{}</Previous User Preference>

<Reflection>{}</Reflection>

You should refine the previous user preference considering the reflection.

Summarize user preference on books in 200 words. You should think step by step."""


#####################dataset construction#####################
### movie
"""You are a helpful assistant for recommender system. Your task is to determine if the user will like the target movie.

We will provide you with the following information:
- The user's historical interactions in the format [MOVIE NAME (YEAR), RATING], where a RATING greater than 3 indicates a like, and a RATING of 3 or less indicates a dislike.
- The target movie's name.
- Your previous summarized user preference.
- Reflection on your previous summarized user preference.

<User History>{}</User  History>

<Target Movie Name>{}</Target Movie Name>

<Previous user preference>{}</Previous user preference>

<Reflection>{}</Reflection>

You should refine the previous user preference considering the reflection and give the final correct answer.

Please strictly follow the following format:
<Refined user preference> [Summarize user preference here in 200 words. Do not include any information about the target movie please. You should think step by step.] </Refined user preference>
<Final Verdict> ["user will like the target movie" or "user will not like the target movie" here] </Final Verdict>
"""

##################### fine-tune #####################
### movie
"""You are an expert recommender engine. Your task is to inference the user preference.

We will provide you with the following information:
- The user's historical interactions in the format [MOVIE NAME (YEAR), RATING], where a RATING greater than 3 indicates a like, and a RATING of 3 or less indicates a dislike.
- Your previous summarized user preference.
- Reflection on your previous summarized user preference.

<User History>{}</User History>

<Previous User Preference>{}</Previous User Preference>

<Reflection>{}</Reflection>

You should refine the previous user preference considering the reflection.

Summarize user preference on movies in 200 words. You should think step by step."""

## Amz && Movie Item Refining
###################dataset construction#######################
### amz

"""You are an expert recommender engine. Your task is to determine if the target user will like the target book.

We will provide you with the following information:
- The target book's name.
- The historical interactions of one user who likes the book and one user who does not. The historical interactions are in the format [Book NAME, RATING], where a RATING greater than 4 indicates a like, and a RATING of 4 or less indicates a dislike.
- The historical interactions of the target user.
- Your previous summarized target book knowledge.
- Reflection on your previous summarized target book knowledge.

<Target Book Name>{}</Target Book Name>

<Like User History>{}</Like User History>

<Dislike User History>{}</Dislike User History>

<Target User History>{}</Target User History>

<Previous Book Knowledge>{}</Previous Book Knowledge>

<Reflection>{}</Reflection>

You should refine the previous book knowledge considering the reflection and give the final correct answer.

Please strictly follow the following format:
<Refined Book Knowledge>[Summarize your knowledge about the target book in 200 words. Include the following: 1. The book's basic attributes, such as genre, author, writing style, theme, and setting. 2. The characteristics of users who like the target book. 3. The characteristics of users who dislike the target book. Do not include any information about the target user. You should think step by step.]</Refined Book Knowledge>
<Final Verdict>["target user will like the target book" or "target user will not like the target book" here]</Final Verdict>
"""

##################### fine-tune #####################
### amz
"""You are an expert recommender engine. Your task is to inference knowledge about the target book.

We will provide you with the following information:
- The target book's name.
- The historical interactions of one user who likes the book and one user who does not. The historical interactions are in the format [Book NAME, RATING], where a RATING greater than 4 indicates a like, and a RATING of 4 or less indicates a dislike.
- Your previous summarized target book knowledge.
- Reflection on your previous summarized target book knowledge.

<Target Book Name>{}</Target Book Name>

<Like User History>{}</Like User History>

<Dislike User History>{}</Dislike User History>

<Previous Book Knowledge>{}</Previous Book Knowledge>

<Reflection>{}</Reflection>

You should refine the previous book knowledge considering the reflection.

Summarize your knowledge about the target book in 200 words. Include the following: 1. The book's basic attributes, such as genre, author, writing style, theme, and setting. 2. The characteristics of users who like the target book. 3. The characteristics of users who dislike the target book. You should think step by step."""


#####################dataset construction#####################
### movie
"""You are an expert recommender engine. Your task is to determine if the target user will like the target movie.

We will provide you with the following information:
- The target movie's name.
- The historical interactions of one user who likes the target movie and one user who does not. The historical interactions are in the format [MOVIE NAME (YEAR), RATING], where a RATING greater than 3 indicates a like, and a RATING of 3 or less indicates a dislike.
- The historical interactions of the target user.
- Your previous summarized target movie knowledge.
- Reflection on your previous summarized target movie knowledge.

<Target Movie Name>{}</Target Movie Name>

<Like User History>{}</Like User History>

<Dislike User History>{}</Dislike User History>

<Target User History>{}</Target User History>

<Previous Movie Knowledge>{}</Previous Movie Knowledge>

<Reflection>{}</Reflection>

You should refine the previous movie knowledge considering the reflection and give the final correct answer.

Please strictly follow the following format:
<Refined Movie Knowledge>[Summarize your knowledge about the target movie in 200 words. Include the following: 1.The target movie's basic attributes, such as genre, director/cast, country, character, plot/theme, mood/tone, critical acclaim/award. 2.The characteristics of users who like the movie. 3. The characteristics of users who dislike the movie. Do not include any information about the target user. You should think step by step.]</Refined Movie Knowledge>
<Final Verdict>["target user will like the target movie" or "target user will not like the target movie" here]</Final Verdict>
"""

##################### fine-tune #####################
### movie
"""You are an expert recommender engine. Your task is to inference knowledge about the target movie.

We will provide you with the following information:
- The target movie's name.
- The historical interactions of one user who likes the target movie and one user who does not. The historical interactions are in the format [MOVIE NAME (YEAR), RATING], where a RATING greater than 3 indicates a like, and a RATING of 3 or less indicates a dislike.
- Your previous summarized target movie knowledge.
- Reflection on your previous summarized target movie knowledge.

<Target Movie Name>{}</Target Movie Name>

<Like User History>{}</Like User History>

<Dislike User History>{}</Dislike User History>

<Previous Movie Knowledge>{}</Previous Movie Knowledge>

<Reflection>{}</Reflection>

You should refine the previous movie knowledge considering the reflection.

Summarize your knowledge about the target movie in 200 words. Include the following: 1.The target movie's basic attributes, such as genre, director/cast, country, character, plot/theme, mood/tone, critical acclaim/award. 2.The characteristics of users who like the movie. 3. The characteristics of users who dislike the movie. You should think step by step."""
