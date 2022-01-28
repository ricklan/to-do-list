import React from "react";
import { Link, useLocation } from "react-router-dom";

const axios = require("axios");
let username;

function getTasks(pageNum, filter = null) {
  let data = { username: username, pageNumber: pageNum };
  if (filter) {
    data.filter = filter;
  }

  axios
    .get("http://127.0.0.1:5000/api/getTask", { params: data })
    .then((response) => {
      displayTasks(response.data);
    })
    .catch((error) => {
      console.log(error.response.data);
    });
}

function displayTasks(tasks) {
  let taskWrapper = document.getElementById("displayed-tasks");
  if (tasks.length === 0) {
    taskWrapper.innerHTML = "No tasks";
  }
}

function Dashboard() {
  const { state } = useLocation();
  username = state.username;
  let curPage = 1;
  getTasks(curPage);

  return (
    <>
      <p>{username}</p>
      <p>filter will go here</p>
      <button>
        <Link to="/">Log Out;</Link>
      </button>
      <br />
      <section>
        <button>left</button>
        <div id="displayed-tasks"> tasks will go here</div>
        <button>right</button>
      </section>
      <button>New Task</button>
    </>
  );
}

export default Dashboard;
