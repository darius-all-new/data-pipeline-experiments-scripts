/*
 Cloudflare worker for retrieving data from InfluxDB
 */

addEventListener("fetch", (event) => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const token = "YOUR INFLUXDB TOKEN";
  const org = "INFLUXDB ORG";
  const bucket = "INFLUXDB BUCKET";
  const url = "INFLUXDB URL";

  // Adapt this query to suit your own needs (e.g. time range, data structure etc.):
  const query = `
    from(bucket: "${bucket}")
    |> range(start: -60m)
    |> filter(fn: (r) =>
      r._measurement == "enviro" and
      (r._field == "temperature" or r._field == "humidity" or r._field == "pressure")
    )
    `;

  try {
    const response = await fetch(`${url}/api/v2/query?org=${org}`, {
      method: "POST",
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      throw new Error(`Failed to query InfluxDB: ${response.statusText}`);
    }

    const data = await response.text();
    console.log(data);

    const lines = data.split("\r\n");
    const extractedData = [];

    // ******************************************************************
    // Some adaption may be needed here if you change the data structure:
    // ******************************************************************
    for (const line of lines) {
      const values = line.split(",");
      const time = values[5];
      const value = parseFloat(values[6]);
      extractedData.push({ time: time, [values[7]]: value });
    }

    const mergedArray = [];

    extractedData.forEach((obj) => {
      const existingObj = mergedArray.find((item) => item.time === obj.time);

      if (existingObj) {
        Object.assign(existingObj, obj);
      } else {
        mergedArray.push(obj);
      }
    });

    return new Response(JSON.stringify(mergedArray), {
      headers: {
        "Access-Control-Allow-Origin": "*", // Change this to your own trusted domains
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json",
      },
    });
  } catch (error) {
    console.error("Failed to query InfluxDB:", error);

    return new Response(JSON.stringify([]), {
      headers: {
        "Access-Control-Allow-Origin": "*", // Change this to your own trusted domains
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json",
      },
    });
  }
}
