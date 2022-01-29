import React from "react";

function EditTask({ task, handleClose }) {
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
  }
  return (
    <>
      <h2>New Task</h2>
      <button onClick={handleClose}>Close</button>
      <form>
        <input type="text" name="title" defaultValue={task ? task.title : ""} />
        <div>Add Title</div>
        <br />
        <textarea
          name="description"
          defaultValue={task ? task.description : ""}
        ></textarea>
        <div>Enter description...</div>
        <p>0/100</p>
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
        </div>
        <button>Create</button>
      </form>
    </>
  );
}

export default EditTask;
