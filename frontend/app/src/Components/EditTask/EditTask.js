import React from "react";
import "./EditTask.css";
import tasqueManager from "../../images/tasque-manager-png.png";

const axios = require("axios");

function handleSubmit(e, task, handleClose) {
  e.preventDefault();
  task.title = e.target.title.value;
  task.description = e.target.description.value;
  if (e.target.priority.value) {
    task.priority = e.target.priority.value;
    document.getElementById("priority-error").innerHTML = "";
    if (task.taskID) {
      updateTask(task, handleClose);
    } else {
      addTask(task, handleClose);
    }
  } else {
    document.getElementById("priority-error").innerHTML =
      "Please select a priority";
  }
}

function updateTask(task, handleClose) {
  axios
    .patch("http://127.0.0.1:5000/api/editTask", task)
    .then(() => {
      handleClose();
    })
    .catch((error) => {
      console.log(error.message);
    });
}

function addTask(task, handleClose) {
  axios
    .post("http://127.0.0.1:5000/api/addTask", task)
    .then(() => {
      handleClose();
    })
    .catch((error) => {
      console.log(error.message);
    });
}

function updateCount(length) {
  let countTag = document.getElementById("desc-count");
  countTag.innerHTML = length + "/100";
}

function EditTask({ task, handleClose, username }) {
  if (!task) {
    task = { title: "", description: "", priority: null, username: username };
  }

  return (
    <>
      <div className="popup-wrapper">
        <div className="popup-window">
          <div className="heading">
            <h2>{task.taskID ? "Update Tasque" : "New Tasque"}</h2>
            <button onClick={handleClose}>X</button>
          </div>
          <form onSubmit={(e) => handleSubmit(e, task, handleClose)}>
            <div className="text-fields-and-tasque">
              <div className="text-fields">
                <div className="title">
                  <label>Title:</label>
                  <input type="text" name="title" defaultValue={task.title} />
                </div>
                <br />
                <div className="description">
                  <div>
                    <label>Description:</label>
                    <textarea
                      name="description"
                      defaultValue={task.description}
                      maxLength="100"
                      onChange={(e) => updateCount(e.target.value.length)}
                    ></textarea>
                  </div>
                  <p id="desc-count">{task.description.length}/100</p>
                </div>
              </div>
              <img src={tasqueManager} alt="" className="tasque" />
            </div>
            <div className="bottom-row">
              <div className="priority-radio">
                <h3>Priority: </h3>
                <input
                  type="radio"
                  id="priority-high"
                  name="priority"
                  value="H"
                  defaultChecked={task.priority === "H"}
                />
                <label htmlFor="priority-high">High</label>
                <input
                  type="radio"
                  id="priority-medium"
                  name="priority"
                  value="M"
                  defaultChecked={task.priority === "M"}
                />
                <label htmlFor="priority-medium">Medium</label>
                <input
                  type="radio"
                  id="priority-low"
                  name="priority"
                  value="L"
                  defaultChecked={task.priority === "L"}
                />
                <label htmlFor="priority-low">Low</label>
              </div>
              <p id="priority-error"></p>
              <button type="submit">{task.taskID ? "Update" : "Create"}</button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}

export default EditTask;
