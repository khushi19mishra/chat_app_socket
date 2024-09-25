import { useState } from 'react';

export default function Register() {
  const [registerData, setRegisterData] = useState({ username: '', password: '' });
  const [message, setMessage] = useState('');

  const handleRegister = async () => {
    const res = await fetch('http://localhost:5000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(registerData),
    });

    const data = await res.json();
    if (res.status === 201) {
      setMessage('User registered successfully! You can now log in.');
    } else {
      setMessage(`Registration failed: ${data.message || 'Unknown error'}`);
    }
  };

  return (
    <div>
      <h1>Register</h1>
      <input
        type="text"
        placeholder="Username"
        value={registerData.username}
        onChange={(e) => setRegisterData({ ...registerData, username: e.target.value })}
      />
      <input
        type="password"
        placeholder="Password"
        value={registerData.password}
        onChange={(e) => setRegisterData({ ...registerData, password: e.target.value })}
      />
      <button onClick={handleRegister}>Register</button>
      <p>{message}</p>
    </div>
  );
}
