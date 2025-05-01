document.addEventListener(
  "DOMContentLoaded",
  // once the page is loaded
  () => {
    console.log("connecting to the SocketIO backend")
    const socket = io()
    socket.on('connect', () => {
        console.log('Connected!')
        socket.emit('connect-ack', {messages: 'I\'m connected!'})
    socket.on('note-updated', ({ id, done }) => {
      const checkbox = document.querySelector(`input[data-id='${id}']`);
      if (checkbox) {
        checkbox.checked = done;
        }
      });
        
    })
    
document.querySelectorAll(".note>form>input")
      // on every input element inside the form inside the note class
      .forEach((element) => {
        // how to react on its change event
        element.addEventListener("change", (event) => {
          const done = element.checked
          const id = element.dataset.id 
          
          // ask the API to update the note
            fetch(`/api/notes/${id}/done`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ done }),
            })
            .then((response) => response.json())
            .then((data) => {
              if (data.ok) {
              console.log("ok")
              } else {
              console.log(data.status, data)
              }
            })
        })
      })
  },
)
