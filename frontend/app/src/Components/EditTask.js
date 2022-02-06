import React from "react";

const axios = require("axios");

function handleSubmit(e, task, handleClose) {
  e.preventDefault();
  if (task.id) {
    //handle edit task
  }
  //create new task
  else {
    task.title = e.target.title.value;
    task.description = e.target.description.value;
    if (e.target.priority.value) {
      task.priority = e.target.priority.value;
      document.getElementById("priority-error").innerHTML = "";
      addTask(task, handleClose);
    } else {
      document.getElementById("priority-error").innerHTML =
        "Please select a priority";
    }
  }
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

function updateCount(e) {
  let countTag = document.getElementById("desc-count");
  let length = e.target.value.length;
  countTag.innerHTML = length + "/100";
}

function EditTask({ task, handleClose, username }) {
  if (task) {
    switch (task.priority) {
      case "H":
        document.getElementById("priority-high").checked = true;
        break;
      case "M":
        document.getElementById("priority-medium").checked = true;
        break;
      default:
        document.getElementById("priority-low").checked = true;
    }
  } else {
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
          onChange={(e) => updateCount(e)}
        ></textarea>
        <div>Enter description...</div>
        <p id="desc-count">0/100</p>
        <div>
          <input type="radio" id="priority-high" name="priority" value="H" />{" "}
          High
          <input
            type="radio"
            id="priority-medium"
            name="priority"
            value="M"
          />{" "}
          Medium
          <input type="radio" id="priority-low" name="priority" value="L" /> Low
          <p id="priority-error"></p>
        </div>
        <button type="submit">Create</button>
      </form>
    </>
  );
}

export default EditTask;
