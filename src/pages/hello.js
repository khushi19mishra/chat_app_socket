// // pages/index.js
// import { useState, useEffect } from 'react';
// import io from 'socket.io-client';

// // Connect to the Flask Socket.IO server explicitly
// const socket = io('http://localhost:5000');  // Flask backend URL

// export default function Home() {
//   const [message, setMessage] = useState('');
//   const [messages, setMessages] = useState([]);

//   useEffect(() => {
//     // Listen for incoming messages from the server
//     socket.on('message', msg => {
//       setMessages(prevMessages => [...prevMessages, msg]);
//     });

//     // Clean up the socket connection on component unmount
//     return () => {
//       socket.off('message');
//     };
//   }, []);

//   const sendMessage = () => {
//     // Send the message to the server
//     socket.emit('message', message);
//     setMessage('');  // Clear the input field
//   };

//   return (
//     <div>
//       <h1>Chat App</h1>
//       <div>
//         {messages.map((msg, index) => (
//           <p key={index}>{msg}</p>
//         ))}
//       </div>
//       <input
//         type="text"
//         value={message}
//         onChange={e => setMessage(e.target.value)}
//       />
//       <button onClick={sendMessage}>Send</button>
//     </div>
//   );
// }


// pages/index.js

import { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

export default function Home() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    // Fetch previous messages when the client connects
    socket.on('previous_messages', (previousMessages) => {
      setMessages(previousMessages);
    });

    // Listen for new messages
    socket.on('message', (msg) => {
      setMessages((prevMessages) => [...prevMessages, msg]);
    });

    // Clean up when the component unmounts
    return () => {
      socket.off('previous_messages');
      socket.off('message');
    };
  }, []);

  const sendMessage = () => {
    // Assuming a hardcoded username for simplicity; in a real app, you'd have user authentication
    const username = 'username';
    socket.emit('message', { username, message });
    setMessage('');
  };

  return (
    <div>
      <h1>Chat App</h1>
      <div>
        {messages.map((msg, index) => (
          <p key={index}>
            <strong>{msg.username}:</strong> {msg.message}
          </p>
        ))}
      </div>
      <input
        type="text"
        value={message}
        onChange={e => setMessage(e.target.value)}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}


// import { useState, useEffect } from 'react';
// import io from 'socket.io-client';

// const socket = io('http://localhost:5000');

// export default function Home() {
//   const [message, setMessage] = useState('');
//   const [messages, setMessages] = useState([]);
//   const [username, setUsername] = useState('');
//   const [isLoggedIn, setIsLoggedIn] = useState(false);
//   const [loginData, setLoginData] = useState({ username: '', password: '' });

//   useEffect(() => {
//     // if (isLoggedIn) {
//       // Fetch previous messages when the client connects
//       socket.on('previous_messages', (previousMessages) => {
//         setMessages(previousMessages);
//       });

//       // Listen for new messages
//       socket.on('message', (msg) => {
//         setMessages((prevMessages) => [...prevMessages, msg]);
//       });

//       // Clean up when the component unmounts
//       return () => {
//         socket.off('previous_messages');
//         socket.off('message');
//       };
//     });
// //   }, [isLoggedIn]);

//   const sendMessage = () => {
//     socket.emit('message', { message });
//     setMessage('');
//   };

//   const handleLogin = async () => {
//     const res = await fetch('http://localhost:5000/login', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify(loginData),
//     });

//     const data = await res.json();
//     if (res.status === 200) {
//       setIsLoggedIn(true);
//       setUsername(data.username);
//     } else {
//       alert('Login failed');
//     }
//   };

//   const handleLogout = async () => {
//     await fetch('http://localhost:5000/logout', {
//       method: 'POST',
//     });
//     setIsLoggedIn(false);
//     setUsername('');
//   };

//   return (
//     <div>
//       {!isLoggedIn ? (
//         <div>
//           <h1>Login</h1>
//           <input
//             type="text"
//             placeholder="Username"
//             value={loginData.username}
//             onChange={(e) => setLoginData({ ...loginData, username: e.target.value })}
//           />
//           <input
//             type="password"
//             placeholder="Password"
//             value={loginData.password}
//             onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
//           />
//           <button onClick={handleLogin}>Login</button>
//         </div>
//       ) : (
//         <div>
//           <h1>Chat App - Welcome {username}</h1>
//           <div>
//             {messages.map((msg, index) => (
//               <p key={index}>
//                 <strong>{msg.username}:</strong> {msg.message}
//               </p>
//             ))}
//           </div>
//           <input
//             type="text"
//             value={message}
//             onChange={e => setMessage(e.target.value)}
//           />
//           <button onClick={sendMessage}>Send</button>
//           <button onClick={handleLogout}>Logout</button>
//         </div>
//       )}
//     </div>
//   );
// }
