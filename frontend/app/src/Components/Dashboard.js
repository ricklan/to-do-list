import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import EditTask from "./EditTask";

const axios = require("axios");
let username;

/**
 * Makes a get request to the to-do-list api to retrieve data based on pageNum and
 * filter.
 * @param {number} pageNum - the page number of the tasks to retrieve
 * @param {String} filter - the filter to apply to the tasks (H, M or L)
 */
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

/**
 * Displays the given list of tasks on the screen.
 * @param {Array} tasks the list of tasks to display
 */
function displayTasks(tasks) {
  let taskWrapper = document.getElementById("displayed-tasks");
  if (tasks.length === 0) {
    taskWrapper.innerHTML = "No tasks";
  }
}

function Dashboard() {
  const { state } = useLocation();
  username = state.username;
  const [taskData, editTask] = useState(null);
  const [taskEditIsOpen, setTaskEditIsOpen] = useState(false);

  const toggleEditTaskPopup = () => {
    setTaskEditIsOpen(!taskEditIsOpen);
  };

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
      <button onClick={toggleEditTaskPopup}>New Task</button>
      {taskEditIsOpen && (
        <EditTask task={taskData} handleClose={toggleEditTaskPopup} />
      )}
    </>
  );
}

export default Dashboard;
