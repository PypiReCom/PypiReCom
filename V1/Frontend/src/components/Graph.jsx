
import React, { useEffect } from "react";
import Graph from "graphology";
import Sigma from "sigma";

const GraphComponent = (props) => {
  useEffect(() => {
    const data=props.data;
  console.log("final",data);

    const container = document.getElementById("sigma-container");
    const graph = new Graph();

    const nodeSizes = { "Package": 10, "Dependency": 7, "License": 5 }; // Define sizes for each node type

    const nodeColors = { "Package": "green", "Dependency": "pink", "License": "lightblue" };

    const addNode = (id, type, size) => {
      if (!graph.hasNode(id)) {
        graph.addNode(id, { label: id, color: nodeColors[type] || "gray", size: size });
      }
    };

    const addEdge = (source, target, type, label, color) => {
      graph.addEdge(source, target, { type, label, size: 4, color });
    };

    console.log("data", typeof(data));

    data.result.forEach(item => {
      addNode(item.v_id, item.v_type, nodeSizes[item.v_type] || 5); // Set size based on node type
    });

    data.Package_Dependency.forEach(item => {
      addNode(item.package, "Package", nodeSizes["Package"]);
      addNode(item.dependency, "Dependency", nodeSizes["Dependency"]);
      addEdge(item.package, item.dependency, "line", 'has_dependency', "#ccc");
    });

    data.Package_License.forEach(item => {
      const licenseNode = `License-${item.license}`;
      addNode(item.package, "Package", nodeSizes["Package"]);
      addNode(licenseNode, "License", nodeSizes["License"]);
      addEdge(item.package, licenseNode, "arrow", "license", "#ccc");
    });

    const packageNodes = graph.nodes().filter(node => graph.getNodeAttribute(node, 'color') === 'green');

    packageNodes.forEach(packageNode => {
      const centerX = Math.random() * 200;
      const centerY = Math.random() * 200;
      const radius = 25 + Math.random()*50; // Adjusted radius for compactness

      graph.mergeNodeAttributes(packageNode, { x: centerX, y: centerY });

      const dependencies = graph.neighbors(packageNode).filter(neighbor => graph.getNodeAttribute(neighbor, 'color') === 'pink');
      const licenses = graph.neighbors(packageNode).filter(neighbor => graph.getNodeAttribute(neighbor, 'color') === 'lightblue');

      dependencies.forEach((dependency, index) => {
        const angle = Math.random() * Math.PI / 10;
        const x = centerX + radius * Math.cos(angle);
        const y = centerY + radius * Math.sin(angle);
        graph.mergeNodeAttributes(dependency, { x, y });
      });

      licenses.forEach((license, index) => {
        const angle = (Math.random() * Math.PI / 10) + Math.PI / 10;
        const x = centerX + radius * Math.cos(angle);
        const y = centerY + radius * Math.sin(angle);
        graph.mergeNodeAttributes(license, { x, y });
      });
    });

    const renderer = new Sigma(graph, container, {
      renderEdgeLabels: true,
      defaultEdgeLabelColor: "#000000",
      settings: {
        autoRescale: true,
        drawEdges: true,
        drawLabels: true,
        drawEdgeLabels: true,
        labelThreshold: 1,
        labelSize: 'fixed',
        labelSizeRatio: 1,
        labelFont: 'Roboto',
        labelColor: 'default',
        enableEdgeHovering: true,
        edgeHoverPrecision: 5,
        edgeHoverSizeRatio: 1,
        edgeHoverHighlightNodes: "circle",
        minNodeSize: 5, // Adjust node size
        maxNodeSize: 20, // Adjust node size
        defaultNodeColor: "#ec5148",
        defaultEdgeColor: "#aaa",
        defaultNodeHoverColor: "#fc4e2a",
        defaultEdgeHoverColor: "#000",
        zoomMin: 0.01,
        zoomMax: 1,
        edgeColor: "default",
        minEdgeSize: 0.5,
        maxEdgeSize: 5,
        borderSize: 1,
        defaultNodeBorderColor: "#000",
        enableHovering: true,
        singleHover: true,
        hoverFont: "12px Arial",
        font: "12px Arial",
      },
    });

    renderer.on('overNode', (event) => {
      const nodeId = event.data.node;
      const neighbors = graph.neighbors(nodeId);
      const nodesToChangeColor = graph.nodes().filter(node => !neighbors.includes(node) && node !== nodeId);
      
      nodesToChangeColor.forEach(node => {
        renderer.graph.nodesAttributes(node.id).color = "#ffffff"; // Change color to white
      });

      renderer.refresh();
    });

    renderer.on('outNode', () => {
      graph.nodes().forEach(node => {
        renderer.graph.nodesAttributes(node.id).color = nodeColors[node.id.split("-")[0]] || "gray"; // Restore original color
      });

      renderer.refresh();
    });

    return () => {
      renderer.kill();
    };
  }, []);

  // return <div id="sigma-container" style={{ height: "800px", backgroundColor: "#f9f9f9" }}></div>;
  return <div id="sigma-container" style={{ height: "300px", width: "100%"}}></div>;

};

export default GraphComponent;