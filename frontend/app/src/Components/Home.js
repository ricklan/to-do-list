import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import Login from "./Login";
import SignUp from "./SignUp";
import { BrowserRouter } from "react-router-dom";

function Home() {
  return (
    <BrowserRouter>
      <div className="login">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
        </Routes>
      </div>
      {/* <Login /> */}
      {/* <SignUp /> */}
    </BrowserRouter>
  );
}

export default Home;
