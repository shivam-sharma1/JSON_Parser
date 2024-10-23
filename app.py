from flask import Flask, request, jsonify
from Parser import JSONTokenizer, JSONParser  # Import the custom JSON parser

app = Flask(__name__)

@app.route('/parse-json', methods=['POST'])
def parse_json():
    try:
        # Get the raw JSON string from the request body
        json_string = request.json.get("json")
        
        # Tokenize and parse the JSON string
        tokenizer = JSONTokenizer(json_string)
        tokens = tokenizer.tokenize()

        parser = JSONParser(tokens)
        parsed_object = parser.parse()

        # Return the parsed object as JSON
        return jsonify({"result": parsed_object})
    
    except Exception as e:
        # Return the error message if parsing fails
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
