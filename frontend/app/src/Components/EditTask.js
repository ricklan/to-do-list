import React from "react";

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
      <h2>New Task</h2>
      <button onClick={handleClose}>Close</button>
      <form onSubmit={(e) => handleSubmit(e, task, handleClose)}>
        <input type="text" name="title" defaultValue={task.title} />
        <div>Add Title</div>
        <br />
        <textarea
          name="description"
          defaultValue={task.description}
          maxLength="100"
          onChange={(e) => updateCount(e.target.value.length)}
        ></textarea>
        <div>Enter description...</div>
        <p id="desc-count">{task.description.length}/100</p>
        <div>
          <input
            type="radio"
            id="priority-high"
            name="priority"
            value="H"
            defaultChecked={task.priority === "H"}
          />
          High
          <input
            type="radio"
            id="priority-medium"
            name="priority"
            value="M"
            defaultChecked={task.priority === "M"}
          />
          Medium
          <input
            type="radio"
            id="priority-low"
            name="priority"
            value="L"
            defaultChecked={task.priority === "L"}
          />
          Low
          <p id="priority-error"></p>
        </div>
        <button type="submit">{task.taskID ? "Update" : "Create"}</button>
      </form>
    </>
  );
}

export default EditTask;
