### Interview Assignment: Chat Application with React and Next.js

**Objective:**
The goal of this assignment is to develop a simple chat application using a React + Next.js frontend that interacts with a provided backend. The backend is already deployed, and you will integrate it with your frontend using the given APIs. Authentication should be handled with JWT tokens.

**Backend Information:**
- **API Base URL:** `http://3.109.213.173:5000/api/`
- **API Documentation:** Available via Swagger (You can explore and test the API endpoints here).

**Authentication:**  
You will use JWT tokens for authentication throughout the frontend.

---

### Backend Workflow for Testing:

1. **Register Users:**
   - Create multiple users via the `/api/register/` endpoint.
   
2. **List Registered Users:**
   - Use a GET request on `/api/users/` to see all registered users (Take note of the user IDs).

3. **User Login:**
   - Log in using `/api/login/`.
     - You will receive:
       - An access token (an unsigned JWT token) for authentication.
       - A refresh token (can be ignored for this task).

4. **Create a Chatroom:**
   - Use a POST request on `/api/chatroom/create/`.
   - Pass user IDs to add them to the chatroom. For one-on-one chats, include two user IDs.

5. **Send Messages:**
   - Use the `/api/chatroom/{chatroom_id}/send/` endpoint to send a message within the chatroom.

6. **Verify Messages:**
   - Retrieve messages using the `/api/chatroom/{chatroom_id}/messages/` endpoint.

7. **Testing as Another User:**
   - Log in as another user and confirm that this user can see the chatroom and view the messages.

---

### Assignment Requirements:

1. **Login and Logout Functionality:**
   - Create a simple login/logout page that uses JWT tokens for authentication.

2. **Post-login:**
   - After logging in, the user should be redirected to the chatroom app.

3. **Chatroom Application Features:**
   - **Create Chatrooms:**
     - The logged-in user should be able to view all registered users and select them to create a new chatroom.
   - **Send Messages:**
     - Users should be able to send messages in a chatroom.
   - **Receive Messages:**
     - Users should be able to receive messages, with the chat automatically refreshing every 5 seconds to display new messages.

---

### Notes:
- **No User Registration Page is Required:**
   - You don't need to implement a registration page. User creation should be done via the backend APIs.
   
- **Focus on JWT Authentication:**
   - Ensure that the login and logout functionality is implemented securely using JWT tokens.

By following these steps, you will create a functional chat application using React and Next.js that integrates with the provided backend.