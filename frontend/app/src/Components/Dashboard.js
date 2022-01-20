import React from "react";
import { Link } from "react-router-dom";

function Dashboard() {
  return (
    <>
      <h1>Tasks</h1>
      <button>
        <Link to="/">Log Out;</Link>
      </button>
    </>
  );
}

export default Dashboard;
