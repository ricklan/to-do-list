import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import EditTask from "./EditTask";

const axios = require("axios");
let username;
let curPage = 1;
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
      //if this is the last page, hide the right button
      //if this is the first page, hide the left button
    })
    .catch((error) => {
      console.log(error);
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
  } else {
    taskWrapper.innerHTML = "";
    tasks.forEach((task) => {
      let priorityTask;
      if (task.priority === "H") {
        priorityTask = "task-high";
      } else if (task.priority === "M") {
        priorityTask = "task-medium";
      } else {
        priorityTask = "task-low";
      }
      taskWrapper.innerHTML += `<div id={task-${task.taskID} class=${priorityTask}}>
        <h3>${task.title}</h3>
        <p>${task.description}</p>
        <button>complete</button>
        <button>edit</button>
        <button>delete</button>
      </div>`;
    });
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
        <button
          className="button-hide"
          onClick={() => {
            curPage--;
            getTasks(curPage);
          }}
        >
          left
        </button>
        <div id="displayed-tasks"></div>
        <button
          className="button-hide"
          onClick={() => {
            curPage++;
            getTasks(curPage);
          }}
        >
          right
        </button>
      </section>
      <button onClick={toggleEditTaskPopup}>New Task</button>
      {taskEditIsOpen && (
        <EditTask
          task={taskData}
          handleClose={toggleEditTaskPopup}
          username={username}
        />
      )}
    </>
  );
}

export default Dashboard;
