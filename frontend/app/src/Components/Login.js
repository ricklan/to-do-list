import React from "react";
import { Link } from "react-router-dom";

function Login() {
  return (
    <>
      <h3>Log In</h3>
      <form>
        <div>
          <label> Username:</label>
          <input type="text" name="username" id="name" required></input>
        </div>
        <div>
          <label> Passsword:</label>
          <input type="text" name="password" id="password" required></input>
        </div>
        <button>Log In</button>
      </form>
      <Link to="/SignUp">Sign Up</Link>
    </>
  );
}

export default Login;