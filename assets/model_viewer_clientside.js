// assets/model_viewer_clientside.js

const _modelViewerLogic = {

  svgElements: {},

  // Add 'hotspotsProp' as an argument (we don't actually use its value, but need it for the Input)
  _updateDimensionsImpl: function(newSrc, checkboxValue, selectedUnit, hotspotsProp, modelViewerId, containerId) {
    const modelViewer = document.getElementById(modelViewerId);
    const container = document.getElementById(containerId);

    // --- FIX: Directly use the boolean value from dmc.Checkbox ---
    // const show = checkboxValue.includes('show'); // Old line for dcc.Checklist
    const show = !!checkboxValue; // Convert checkboxValue (True/False) to boolean 'show'
    // console.log(`Clientside Update. Show=${show}, Unit=${selectedUnit}`); // Keep for Debug

    if (!modelViewer || !container) { /* Error check */ return window.dash_clientside.no_update; }

    // --- Get or Create SVG ---
    let svg = this.svgElements[modelViewerId]?.svg;
    let dimLines = this.svgElements[modelViewerId]?.lines;
    const svgNs = 'http://www.w3.org/2000/svg';
    if (!svg) { /* Create SVG/Lines */
      // console.log("Creating SVG elements"); // Debug
      svg = document.createElementNS(svgNs, 'svg'); /* ... attributes ... */
      svg.setAttribute('id', `${modelViewerId}-svg`);
      svg.setAttribute('width', '100%'); svg.setAttribute('height', '100%');
      Object.assign(svg.style, { position: 'absolute', top: '0', left: '0', pointerEvents: 'none', display: 'block', zIndex: 1 }); // Added zIndex
      dimLines = [];
      // Ensure enough lines for the JS logic (JS uses indices 0-4)
      for (let i = 0; i < 5; i++) { /* create lines */
          const line = document.createElementNS(svgNs, 'line'); line.setAttribute('class', 'dimensionLine');
          line.setAttribute('x1','0'); line.setAttribute('y1','0'); line.setAttribute('x2','0'); line.setAttribute('y2','0');
          svg.appendChild(line); dimLines.push(line);
      }
      container.appendChild(svg); this.svgElements[modelViewerId] = { svg: svg, lines: dimLines };
    }

    // --- Helper Functions ---

    // UPDATE HOTSPOT: Sets position and text ONLY. NO visibility logic.
    const updateHotspot = (name, position, text) => {
        // Query within the model-viewer element using the slot
        const hotspot = modelViewer.querySelector(`div.hotspot[slot="${name}"]`);
        if (hotspot) { // Check if hotspot element currently exists in DOM
            // Use try-catch for updateHotspot as it might not exist on all versions
            try { modelViewer.updateHotspot({ name: name, position: position }); }
            catch(e) { hotspot.setAttribute('data-position', position); }
            hotspot.textContent = text || '';
            // console.log(`Updated hotspot ${name} pos: ${position} text: ${text}`); // Debug
        } else {
            // If hotspot doesn't exist (because server removed it), do nothing.
             // console.log(`Hotspot ${name} not found in DOM for update.`); // Debug
        }
    };

    // DRAW LINE: Handles coordinates AND line visibility based on 'show'.
    const drawLine = (svgLine, dot1Name, dot2Name, dimName) => {
        // Important: Only query hotspots if 'show' is true, otherwise points might be gone
        const dot1 = show ? modelViewer.queryHotspot(dot1Name) : null;
        const dot2 = show ? modelViewer.queryHotspot(dot2Name) : null;
        const dimHotspot = show && dimName ? modelViewer.queryHotspot(dimName) : null;

        if (svgLine && dot1?.canvasPosition && dot2?.canvasPosition) {
            svgLine.setAttribute('x1', dot1.canvasPosition.x); svgLine.setAttribute('y1', dot1.canvasPosition.y);
            svgLine.setAttribute('x2', dot2.canvasPosition.x); svgLine.setAttribute('y2', dot2.canvasPosition.y);
            const facingCamera = !dimHotspot || dimHotspot.facingCamera;
            // Line visibility depends on show flag AND facingCamera
            if (show && facingCamera) {
                svgLine.classList.remove('hide');
                // console.log(`Drew line between ${dot1Name} and ${dot2Name}`); // Debug
            } else {
                svgLine.classList.add('hide'); // Hide if !show or not facing
            }
        } else {
            if(svgLine) svgLine.classList.add('hide'); // Hide if points not ready/found
             // if(show) console.log(`Could not draw line between ${dot1Name} and ${dot2Name}. Missing points?`, dot1, dot2); // Debug
        }
    };

    // RENDER SVG: Calls drawLine.
    const renderSVG = () => {
        // Ensure lines exist and model is ready enough to query hotspots
        if (!modelViewer.loaded || !dimLines || dimLines.length < 5) return;
        // console.log("Rendering SVG..."); // Debug
        try { /* Draw lines - Using names from python structure */
             drawLine(dimLines[0], 'hotspot-dot+X-Y+Z', 'hotspot-dot+X-Y-Z', 'hotspot-dim+X-Y'); // Z length on +X side
             // Line 1 seems intended for Y height on +X side (connecting +X-Y-Z and +X+Y-Z)
             drawLine(dimLines[1], 'hotspot-dot+X-Y-Z', 'hotspot-dot+X+Y-Z', 'hotspot-dim+X-Z'); // Y height on +X side
             // Line 2 seems intended for X width on +Y side (connecting +X+Y-Z and -X+Y-Z)
             drawLine(dimLines[2], 'hotspot-dot+X+Y-Z', 'hotspot-dot-X+Y-Z', null); // No specific dim text associated?
             // Line 3 seems intended for Y height on -X side (connecting -X+Y-Z and -X-Y-Z)
             drawLine(dimLines[3], 'hotspot-dot-X+Y-Z', 'hotspot-dot-X-Y-Z', 'hotspot-dim-X-Z'); // Y height on -X side
             // Line 4 seems intended for Z length on -X side (connecting -X-Y-Z and -X-Y+Z)
             drawLine(dimLines[4], 'hotspot-dot-X-Y-Z', 'hotspot-dot-X-Y+Z', 'hotspot-dim-X-Y'); // Z length on -X side
        } catch (error) { console.error("Error rendering SVG:", error); }
    };

    // CALCULATE DIMENSIONS: Gets size/center, converts units, calls updateHotspot (pos/text only).
    const calculateAndUpdateDimensions = () => {
        if (!modelViewer.loaded) return;
        // console.log(`Calculating dimensions. Unit: ${selectedUnit}`); // Debug

        // Check if hotspots actually exist in the DOM before trying to calculate
        // We only need to check one, assuming React adds/removes them together
        const firstHotspot = modelViewer.querySelector(`div.hotspot[slot="hotspot-dot+X-Y+Z"]`);
        if (!firstHotspot && show) {
            // console.warn("calculateAndUpdateDimensions called when show=true, but hotspots not found in DOM yet. Retrying shortly."); // Debug
            // Hotspots might not be rendered yet by React after server update. Retry.
            setTimeout(calculateAndUpdateDimensions, 100); // Increased delay slightly
            return;
        }
        if (!show) {
            // console.log("calculateAndUpdateDimensions called when show=false. Skipping calculation."); // Debug
            // If not showing, don't calculate, just ensure lines are hidden via renderSVG later
            renderSVG(); // Ensure lines are hidden based on 'show' = false
            return;
        }

        try {
            const center = modelViewer.getBoundingBoxCenter(); const size = modelViewer.getDimensions();
            if (!size || !center || !size.x || !size.y || !size.z) {
                console.warn("Cannot get valid dimensions/center from modelViewer.");
                // Maybe retry if dimensions aren't ready immediately after load?
                 if (!modelViewer.calculationAttempted) {
                     modelViewer.calculationAttempted = true;
                     setTimeout(calculateAndUpdateDimensions, 200);
                 }
                return;
            }
            modelViewer.calculationAttempted = true; // Mark attempt successful

            const x2 = size.x/2, y2 = size.y/2, z2 = size.z/2;

            let factor = 100, unitLabel = 'cm', precision = 0; // Default to cm
            if (selectedUnit === 'mm') { factor = 1000; unitLabel = 'mm'; precision = 0;}
            else if (selectedUnit === 'm') { factor = 1; unitLabel = 'm'; precision = 2; }
            else if (selectedUnit === 'in') { factor = 39.3701; unitLabel = 'in'; precision = 1;}
            else if (selectedUnit === 'ft') { factor = 3.28084; unitLabel = 'ft'; precision = 2;}

            // Update hotspot positions/text ONLY
            // Positions are in meters (model space)
            updateHotspot('hotspot-dot+X-Y+Z', `${center.x + x2} ${center.y - y2} ${center.z + z2}`);
            updateHotspot('hotspot-dot+X-Y-Z', `${center.x + x2} ${center.y - y2} ${center.z - z2}`);
            updateHotspot('hotspot-dot+X+Y-Z', `${center.x + x2} ${center.y + y2} ${center.z - z2}`);
            updateHotspot('hotspot-dot-X+Y-Z', `${center.x - x2} ${center.y + y2} ${center.z - z2}`);
            updateHotspot('hotspot-dot-X-Y-Z', `${center.x - x2} ${center.y - y2} ${center.z - z2}`);
            updateHotspot('hotspot-dot-X-Y+Z', `${center.x - x2} ${center.y - y2} ${center.z + z2}`);

            // Update dimension text hotspots (position offset slightly for visibility)
            // Text is formatted with units
            updateHotspot('hotspot-dim+X-Y', `${center.x + x2 * 1.1} ${center.y - y2 * 1.1} ${center.z}`, `${(size.z * factor).toFixed(precision)} ${unitLabel}`); // Z Length (+X side)
            updateHotspot('hotspot-dim+X-Z', `${center.x + x2 * 1.1} ${center.y} ${center.z - z2 * 1.1}`, `${(size.y * factor).toFixed(precision)} ${unitLabel}`); // Y Height (+X side)
            // updateHotspot('hotspot-dim+Y-Z', `${center.x} ${center.y + y2 * 1.1} ${center.z - z2 * 1.1}`, `${(size.x * factor).toFixed(precision)} ${unitLabel}`); // X Width (Top) - Let's skip this one for now to simplify
            updateHotspot('hotspot-dim-X-Z', `${center.x - x2 * 1.1} ${center.y} ${center.z - z2 * 1.1}`, `${(size.y * factor).toFixed(precision)} ${unitLabel}`); // Y Height (-X side)
            updateHotspot('hotspot-dim-X-Y', `${center.x - x2 * 1.1} ${center.y - y2 * 1.1} ${center.z}`, `${(size.z * factor).toFixed(precision)} ${unitLabel}`); // Z Length (-X side)

            // Render SVG lines AFTER hotspot data is set/updated
            renderSVG();
        } catch (error) { console.error("Error calculating/updating dimensions:", error); }
    };

    // --- Event Listener Setup ---
    // Use a flag to prevent attaching multiple listeners if the callback runs multiple times
    if (!modelViewer.dimensionListenersAttached) {
        const loadHandler = () => { /*console.log("Load event triggered"); */ modelViewer.calculationAttempted = false; calculateAndUpdateDimensions(); }
        // Camera change only needs to re-render SVG, not recalculate everything
        const cameraChangeHandler = () => { /*console.log("Camera change triggered"); */ renderSVG(); }
        modelViewer.addEventListener('load', loadHandler);
        modelViewer.addEventListener('camera-change', cameraChangeHandler);
        modelViewer.dimensionListenersAttached = true; // Set the flag
        // Store handlers to potentially remove them later if needed, though usually not necessary
        modelViewer._dimensionLoadHandler = loadHandler;
        modelViewer._dimensionCameraChangeHandler = cameraChangeHandler;
        // console.log("Dimension listeners attached."); // Debug

        // If model is already loaded when listeners attach, trigger calculation
        if (modelViewer.loaded) {
            // console.log("Model already loaded on listener attach, calculating dimensions."); // Debug
            setTimeout(calculateAndUpdateDimensions, 50); // Short delay just in case
        }
    }

    // --- Final Visibility Control (SVG Only) & Trigger Calculation ---
    if (svg) { // Check if SVG exists
        if (show) {
            // console.log("Final Block: Setting SVG visible."); // Debug
            svg.classList.remove('hide');
            // Ensure calculations run if model is loaded, as hotspots might have just been added by React
            // Or if unit/model changed while dimensions were shown
            if (modelViewer.loaded) {
                 // console.log("Final Block: Model loaded, triggering calculation/render."); // Debug
                 setTimeout(calculateAndUpdateDimensions, 50); // Recalculate/Render slightly deferred
            }
        } else {
            // console.log("Final Block: Setting SVG hidden."); // Debug
            svg.classList.add('hide');
            // Ensure lines are hidden immediately based on the new 'show' = false state
            renderSVG();
        }
    } else {
         // console.log("Final Block: SVG not found."); // Debug
    }

    // No Dash property needs updating from here
    return window.dash_clientside.no_update;
  }
};

// --- Wrapper Function (Namespace) ---
window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.modelViewer = {
    // Update arguments to include hotspotsProp
    updateDimensions: function(newSrc, checkboxValue, selectedUnit, hotspotsProp, modelViewerId, containerId) {
        // Use optional chaining for safety
        if (window._modelViewerLogic?._updateDimensionsImpl) {
            // Pass all arguments through
            return window._modelViewerLogic._updateDimensionsImpl(newSrc, checkboxValue, selectedUnit, hotspotsProp, modelViewerId, containerId);
        } else {
            console.warn("modelViewer logic not ready, retrying...");
            // Retry mechanism
            setTimeout(() => {
                if (window.dash_clientside?.modelViewer?.updateDimensions) {
                    // Pass all arguments in the retry
                    window.dash_clientside.modelViewer.updateDimensions(newSrc, checkboxValue, selectedUnit, hotspotsProp, modelViewerId, containerId);
                }
            }, 100);
            return window.dash_clientside.no_update; // Prevent Dash error during retry
        }
    }
    // Add other clientside functions here if needed
};

// Assign logic object AFTER definition (safer)
window._modelViewerLogic = _modelViewerLogic;