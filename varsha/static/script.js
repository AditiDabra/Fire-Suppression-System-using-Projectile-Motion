const board = document.getElementById('chessboard');

for (let y = -15; y < 15; y++) {
  for (let x = -15; x < 15; x++) {
    const square = document.createElement('div');
    square.className = 'square ' + ((x + y) % 2 === 0 ? 'white' : 'black');
    square.onclick = () => handleClick(x, y);
    board.appendChild(square);
  }
}

function handleClick(x, y) {
  fetch('/simulate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ x, y })
  })
  .then(res => res.json())
  .then(data => {
    if (data.error) {
      alert(data.error);
      return;
    }

    // Plot 3D Trajectory
    Plotly.newPlot('plot3d', [
      {
        x: data.x_vals,
        y: data.y_vals,
        z: data.z_vals,
        type: 'scatter3d',
        mode: 'lines',
        line: { color: 'blue' }
      },
      {
        x: [data.target[0]],
        y: [data.target[1]],
        z: [0],
        type: 'scatter3d',
        mode: 'markers',
        marker: { color: 'red', size: 5 }
      }
    ], {
      title: '3D Trajectory',
      scene: {
        xaxis: { title: 'X' },
        yaxis: { title: 'Y' },
        zaxis: { title: 'Z' }
      }
    });

    // Plot 2D Side View
    Plotly.newPlot('plot2d', [
      {
        x: data.x_vals,
        y: data.z_vals,
        type: 'scatter',
        mode: 'lines',
        line: { color: 'green' }
      }
    ], {
      title: 'Side View (X-Z)',
      xaxis: { title: 'X' },
      yaxis: { title: 'Z' }
    });

    // ✅ Update output parameters
    document.getElementById('x_input').innerText = data.x_input.toFixed(2);
    document.getElementById('y_input').innerText = data.y_input.toFixed(2);
    document.getElementById('v0').innerText = data.v0.toFixed(2);
    document.getElementById('theta').innerText = data.theta.toFixed(2);
    document.getElementById('phi').innerText = data.phi.toFixed(2);
    document.getElementById('t_final').innerText = data.t_final.toFixed(2);
    document.getElementById('disp').innerText = data.disp.toFixed(2);
  })
 
}
