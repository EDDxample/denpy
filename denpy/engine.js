global.vnstate = {
  background: null,
  character: null,
  speaker: null,
  text: "",
};

/**
 * Hides all the annotations defined in `global.vnimages` and triggers
 *  the first `onTextboxClick()` call.
 */
function init() {
  try {
    this.getField("_speakerbox").display = display.hidden;
    for (let i = 0; i < global.vnimages.length; ++i) {
      this.getField("_" + global.vnimages[i]).display = display.hidden;
    }

    this.getField("_textbox").setFocus();
  } catch (e) {
    app.alert(e.toString());
  }
}

/**
 * Displays the current node and advances the `global.vnindex`, then focuses 
 * on the `_focus_restart` field to refresh the PDF's graphic state.
 * 
 * Called via the `onFocus` event of the `_textbox` field.
 */
function onTextboxClick() {
  if (global.vnindex === undefined) global.vnindex = 0;
  try {
    if (global.vnindex < global.vnnodes.length) {
      var node = global.vnnodes[global.vnindex];
      updateGraphics(node);
      global.vnindex++;
    } else {
      app.alert("The end.");
    }

    this.getField("_focus_restart").setFocus();
  } catch (e) {
    app.alert(e.toString());
  }
}

/**
 * Computes the changes to the graphic state of the visual novel and
 * displays them.
 */
function updateGraphics(node) {
  if (node.background && node.background != global.vnstate.background) {
    this.getField("_" + node.background).display = display.visible;
    if (global.vnstate.background) {
      this.getField("_" + global.vnstate.background).display = display.hidden;
    }
    global.vnstate.background = node.background;
  }
  if (node.character !== undefined && node.character != global.vnstate.character) {
    if (node.character) {
      this.getField("_" + node.character).display = display.visible;
    }
    if (global.vnstate.character) {
      this.getField("_" + global.vnstate.character).display = display.hidden;
    }
    global.vnstate.character = node.character;
  }
  if (node.speaker !== undefined && global.vnstate.speaker != node.speaker) {
    var speakerbox = this.getField("_speakerbox");

    if (node.speaker) {
      // TODO: rescale speakerbox
      speakerbox.value = node.speaker;
      speakerbox.display = display.visible;
    } else {
      speakerbox.display = display.hidden;
    }

    global.vnstate.speaker = node.speaker;
  }
  if (node.text != global.vnstate.text) {
    this.getField("_textbox").value = node.text;
    global.vnstate.text = node.text;
  }
}

init();
