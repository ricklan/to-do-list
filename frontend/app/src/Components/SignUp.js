import React from "react";
import { Link } from "react-router-dom";

function SignUp() {
  return (
    <>
      <h3>Sign Up</h3>
      <form>
        <div>
          <label> First Name:</label>
          <input type="text" name="firstname" id="first-name" required></input>
        </div>
        <div>
          <label> Last Name:</label>
          <input type="text" name="lastname" id="last-name" required></input>
        </div>
        <div>
          <label> Username:</label>
          <input type="text" name="username" id="name" required></input>
        </div>
        <div>
          <label> Passsword:</label>
          <input type="text" name="password" id="password" required></input>
        </div>
        <button>Sign Up</button>
      </form>
      <Link to="/">Log In</Link>
    </>
  );
}

export default SignUp;
