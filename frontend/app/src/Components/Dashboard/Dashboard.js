import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import EditTask from "../EditTask/EditTask";
import "./Dashboard.css";

const axios = require("axios");
let username;
let curPage = 1;
let filter = "None";
/**
 * Makes a get request to the to-do-list api to retrieve data based on pageNum and
 * filter.
 * @param {number} pageNum - the page number of the tasks to retrieve
 */
function getTasks(pageNum, editTask, toggleEditTaskPopup) {
  let data = { username: username, pageNumber: pageNum };
  if (filter !== "None") {
    data.filter = filter;
  }

  axios
    .get("http://127.0.0.1:5000/api/getTask", { params: data })
    .then((response) => {
      displayTasks(response.data, pageNum, editTask, toggleEditTaskPopup);
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
function displayTasks(tasks, pageNum, editTask, toggleEditTaskPopup) {
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
      taskWrapper.innerHTML += `<div id=task-${task.taskID} class="task ${priorityTask}">
        <div class="task-content">
          <h3>${task.title}</h3>
          <p>${task.description}</p>
          <div class="task-buttons">
            <button id=task-${task.taskID}-edit-button>edit</button>
            <button id=task-${task.taskID}-delete-button>delete</button>
          </div>
        </div>
      </div>`;
    });
    //add event listeners to each task buttons
    tasks.forEach((task) => {
      //edit
      document
        .getElementById(`task-${task.taskID}-edit-button`)
        .addEventListener("click", () => {
          handleEditTask(task, editTask, toggleEditTaskPopup);
        });

      //delete
      document
        .getElementById(`task-${task.taskID}-delete-button`)
        .addEventListener("click", () => {
          deleteTask(
            { taskID: task.taskID },
            pageNum,
            editTask,
            toggleEditTaskPopup
          );
        });
    });
  }
}

function deleteTask(id, pageNum, editTask, toggleEditTaskPopup) {
  axios
    .delete("http://127.0.0.1:5000/api/deleteTask", { params: id })
    .then((response) => {
      console.log(response.data);
      getTasks(pageNum, editTask, toggleEditTaskPopup);
    })
    .catch((error) => {
      console.log(error.response);
    });
}

function handleEditTask(task, editTask, toggleEditTaskPopup) {
  editTask({
    taskID: task.taskID,
    title: task.title,
    description: task.description,
    priority: task.priority,
  });
  toggleEditTaskPopup();
}

function handleFilter(value, curPage, editTask, toggleEditTaskPopup) {
  if (value) {
    filter = value;
  }
  getTasks(curPage, editTask, toggleEditTaskPopup);
}

function Dashboard() {
  const { state } = useLocation();
  username = state.username;
  const [taskData, editTask] = useState(null);
  const [taskEditIsOpen, setTaskEditIsOpen] = useState(false);

  const toggleEditTaskPopup = () => {
    setTaskEditIsOpen(!taskEditIsOpen);
  };

  getTasks(curPage, editTask, toggleEditTaskPopup);

  return (
    <>
      <header>
        <h1 id="dashboard-logo">Tasque</h1>
        <div id="filter">
          <label>Filter: </label>
          <select
            id="filter-menu"
            onChange={(e) =>
              handleFilter(
                e.target.value,
                curPage,
                editTask,
                toggleEditTaskPopup
              )
            }
          >
            <option value={null}>None</option>
            <option value="H">High</option>
            <option value="M">Medium</option>
            <option value="L">Low</option>
          </select>
        </div>
        <div id="logout-wrapper">
          <button>
            <Link to="/">Log Out</Link>
          </button>
        </div>
      </header>
      <section className="content-wrapper">
        <button
          className="button-nav-fade next-prev-page"
          onClick={() => {
            curPage--;
            getTasks(curPage, editTask, toggleEditTaskPopup);
          }}
        >
          &lt;
        </button>
        <div id="displayed-tasks"></div>
        <button
          className="button-hide next-prev-page"
          onClick={() => {
            curPage++;
            getTasks(curPage, editTask, toggleEditTaskPopup);
          }}
        >
          &gt;
        </button>
      </section>
      <button
        onClick={() => {
          editTask(null);
          toggleEditTaskPopup();
        }}
        className="new-task-button"
      >
        New Task +
      </button>
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
