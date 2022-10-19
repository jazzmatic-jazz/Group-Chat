1. Created the url for the index funtion in the views.py and render the index.html file

2. whenever we refresh the page our root page renders

INDEX.HTML

3. In html we have mentioned the textarea, input field and a submit button. http://127.0.0.1:8000/

4. in script tag it send the request to the websocket at ws://127.0.0.1:8000/ws/sc/ and creates the instance 

5. When our connection gets open then we see the console.log of  'Websocket connection Open'

6. onmessage runs when we recieves the msg from the server.

7. onclose runs when connection closes.

8. our execution starts from document.getElementById. Applied the event on the button onclick our func runs.

9. created the variable to get the dom with id of chat-message-dom. We need the value by .value assigned in the message variable. Then we have to send the message to the server.

10. We need to convert the message to string, we cannot send the object directly to the server.

11. we have set the empty string so after sending the message we get the empty space.

MESSAGE SENT TO THE SERVER (CONSUMERS.PY)

12. We hit or refresh the page our websocket is also connected.

13. Here we get to see the channel Layer and channel name. channel name will be different for every user or tab or client.

14. then we have the both or more channels to the one group name buddies

15. as group_add work asyncronously so converted it using async_to_sync

16. then we accept the channel and then our two way communication works.

17. whenever we close our browser, disconnect runs. the channel will be discarded.

DATA RECEIVE AND SEND

18. Whenever we receive the message from client to server websocket_receive runs and get the msg in the event['text']

19. whatever msg we received we need to send to the buddies group. and send the message to the group_send firstly converting it to async to sync

20. To send the message to the client we have made the handler for the chat.message as chat_message.

21. when we send the message it firstly go message in the index.py then after it comes to server. 

22. Then to send the message to the client use the send method with text- event['message'] as it contains the real message

23. When we send the message from the server to client the onmessage executes. We get the actual message in the event.data

24. Then we get the message as string we need to convert it into object

25. Then we present the message on the screen through queryselector