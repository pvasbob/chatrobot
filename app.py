# import os
# from openai import OpenAI

# client = OpenAI(
#     api_key=os.environ.get("OPENAI_API_KEY"),
# )

# def get_chatgpt_response(query):
#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": query,
#             }
#         ],
#         model="gpt-3.5-turbo",
#     )

#     response = chat_completion.choices[0].message.content
#     return response

# # Example usage
# # user_query = "What is the capital of France?"
# user_query = "UNC chapel Hill"
# chatgpt_response = get_chatgpt_response(user_query)
# print(chatgpt_response)

# ===============================================================


import os
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_chatgpt_response(query):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": query,
            }
        ],
        model="gpt-3.5-turbo",
    )

    response = chat_completion.choices[0].message.content
    return response

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_query = request.form["query"]
        chatgpt_response = get_chatgpt_response(user_query)

        # Save the response to a file
        with open("responses.txt", "a") as file:
            file.write(f"Query: {user_query}\nResponse: {chatgpt_response}\n\n")

        return render_template("results.html", query=user_query, response=chatgpt_response)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)



# ======================================================

import os
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_chatgpt_response(query):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": query,
            }
        ],
        model="gpt-3.5-turbo",
    )

    response = chat_completion.choices[0].message.content
    return response

def save_to_file(query, response):
    # Create the "record" folder if it doesn't exist
    if not os.path.exists("record"):
        os.makedirs("record")

    # Generate a file name based on the query
    file_name = "_".join(query.lower().split())
    file_path = os.path.join("record", f"{file_name}.txt")

    # Save the query and response to the file
    with open(file_path, "w") as file:
        file.write(f"Query: {query}\nResponse: {response}\n")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_query = request.form["query"]
        chatgpt_response = get_chatgpt_response(user_query)

        # Save the query and response to a file
        save_to_file(user_query, chatgpt_response)

        return render_template("results.html", query=user_query, response=chatgpt_response)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)