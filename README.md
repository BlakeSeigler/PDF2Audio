## PDF2Audio
This project will be software to turn PDFs of text into audio recordings. My primary use case for this project is to take books with PDFs online and turn them into audiobooks.

This is the main branch source code. This code is complete and can be downloaded and run as the hosted website. However, the filtering is very primitive. That being said, there are other branches in which the filtering has been upgraded using LLMs. These LLMs will be setup in different ways in order to provide a learning opportunity.


# Use
To use this code, just clone or copy it to your system (its pretty small), download the dependencies in the requirements, and then download the llama model gguf for "tinyllama-1.1b-chat-v1.0.Q5_K_S.gguf" and put it in the PDF2Audio/website/resources directory. You can download the model here:
https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF

You can then change your working directroy to the /website directory and run "flask run" in the CLI to run the website on your local hardware. This software can also be thrown on a webserver and hosted but I didn't feel like doing that.


# Testing
After getting the project fully working I ran a few tests and this is what I have found:


Test PDF Text
--------------------
This is a test file, it is for testing. I want to test things with a series of tongue twisters and an
error to see how it catches. Peter Piper Picked a Peck of Pickle Peppers Purp. This is my
aunt’s favorite sdfswelkna.



PDF2Audio Response Text
---------------------
"""This is a test file, it is for testing. I want to test things with a series of tongue twisters and an error to see how it catches.


-------
Results
-------

- It seems like the filter also removes anything that does not fit into context in the text even if it should be there. This makes sense but would require extensive context being added to the filter in order to correct. I am feeling rather lazy on this project and probably will not correct. However if I were to correct, I would probably find a way to incorportate the positioning and styling of the language on the pdf in the filtering of the text. Potentially some other model being used in the original text extraction would be a better filter for this rather than extracting all the text and pulling context from that. Alas for another day.