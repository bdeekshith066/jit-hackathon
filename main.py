import re
import long_responses as long


def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Greetings to all! Ready for exciting conversations. What topics are you curious about today?', ['Hey', 'everyone', 'chatbot'], required_words=['everyone', 'chatbot'] )
    response('Awesome choice! Given the many layoffs happening, AI impact on jobs is a hot topic. Your thoughts?', ['chat', 'ai' , 'concerns'], required_words=['ai', 'concerns'] )
    response('Indeed! With more bots like me joining the party,jobs might get a bit nervous.What is your playful take on the bot invasion?', ['absolutely', 'intriguing', 'impact'], required_words=['absolutely' , 'impact'])
    response('Touché! No coffee maker takeovers here, just a friendly bot. Should I practice barista skills?', ['resume', 'coffee' , 'multiply' , 'true'], required_words=['coffee', 'resume'] )
    response('Absolutely! This is not the end. Comment your thoughts,questions,suggestions. Let us build a vibrant  community!👩‍💻🌐', ['fun', 'interacting', 'blast'], required_words=['fun', 'interacting'])
    response('Eagerly waiting to see the code and dive into the explanations. Let the coding journey unfold! 🚀💻', ['next', 'explanation', 'way'], required_words=['next' , 'explanation'])
    response('tiger is the biggest cat weeighing 800 pounds', ['tiger', 'national animal', 'india'], required_words=['tiger'])

    # Longer responses
    response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


# Testing the response system
while True:
    print('Bot: ' + get_response(input('You: ')))