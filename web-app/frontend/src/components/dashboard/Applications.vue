<template>
  <div class="p-4 bg-light">
    <h2 class="mb-4">История (в разработке...)</h2>
    <div class="wrapper bg-white vh-100 p-4 rounded-3 border">
      <div class="d-flex justify-content-between mb-3">
        <div class="d-flex dropdown menu">
          <select class="form-select me-2">
            <option>Filter by Date</option>
            <option>Filter by Salary</option>
            <option>Filter by Status</option>
          </select>
          <select class="form-select me-2">
            <option>Descending</option>
            <option>Ascending</option>
          </select>
        </div>
        <button class="btn btn-outline-danger">Reset Filters</button>
      </div>
      <table class="table table-bordered bg-light">
        <thead>
          <tr>
            <th>ID</th>
            <th>Company</th>
            <th>Address</th>
            <th>Date</th>
            <th>Salary</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>001</td>
            <td>Google</td>
            <td>California</td>
            <td>01 Sep 2023</td>
            <td>$150,000</td>
            <td><span class="badge bg-success">Completed</span></td>
          </tr>
          <tr>
            <td>002</td>
            <td>Netflix</td>
            <td>LA</td>
            <td>15 Aug 2023</td>
            <td>$130,000</td>
            <td><span class="badge bg-danger">Rejected</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: "Applications",
};
</script>
