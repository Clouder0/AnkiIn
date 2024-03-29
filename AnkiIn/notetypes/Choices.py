from ..helper.formatHelper import list2str, format_text
from ..note import Note
from ..model import Model
from ..config import dict as conf
from ..config import config_updater


notetype_name = "Choices"
if notetype_name not in conf["notetype"]:
    conf["notetype"][notetype_name] = {}
settings = conf["notetype"][notetype_name]

priority = None


def update_choices_config():
    global settings, priority
    priority = settings.get("priority", 15)


config_updater.append((update_choices_config, 10))


def check(lines: list, extra_params={}) -> bool:
    return len(lines) >= 3 and len(lines[1]) >= 1 and lines[1][0] == "A"


def get(text: str, deck: str, tags: list, extra_params={}) -> Note:
    lines = text.split("\n")
    question = lines[0]
    options = list()
    remark = ""
    i = 1
    while i < len(lines):
        if lines[i][0] != chr(65 + i - 1):
            break
        options.append(format_text(lines[i]))
        i += 1
    if len(options) <= 1:
        raise Exception("Error! Choices with only one option.")
    options = list2str(options)
    if i < len(lines):
        answer = list2str([x for x in lines[i] if ord(x) >= 65 and ord(x) <= 90], "", "")
        i += 1
    else:
        raise Exception("Error! Choices with no answer.")
    if i < len(lines):
        remark = list2str(lines[i:])

    return ChoicesNote(
        question=question,
        options=options,
        answer=answer,
        remark=remark,
        deck=deck,
        tags=tags)


FRONT = r"""<!--tuxzz.20201115.v0.r0-->
<div id="classifyBox" class="classify"><span id="classifyText"></span><span>：</span></div>
<div id="questionBox" class="text">{{Question}}</div>

{{#Options}}
<ol id="optionBox"></ol>
<div id="optionBuffer" style="display:none">{{Options}}</div>
<div id="answerBuffer" style="display:none">{{text:Answer}}</div>
<hr id="hrLine" style="display:none">
<div id="answerBox" style="display:none">Answer：<span id="newAns"></span>（Original Answer:<span id="origAns"></span>）</div>
<div id="remarkBox" style="display:none">Remark：{{Remark}}</div>
<br><button id="submitButton">Submit</button>
{{/Options}}


<script>
(function() {
"use strict";

const date = new Date();
function pseudo_shuffle_inplace(array) {
		let seed = date.getDay() * 60 + date.getMinutes();
    let currentIndex = array.length, temporaryValue, randomIndex;
    seed = seed || 1;
    let random = function() {
      var x = Math.sin(seed++) * 10000;
      return x - Math.floor(x);
    };
    // While there remain elements to shuffle...
    while (0 !== currentIndex) {
      // Pick a remaining element...
      randomIndex = Math.floor(random() * currentIndex);
      currentIndex -= 1;
      // And swap it with the current element.
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }
    return array;
}

const optionBox = document.getElementById("optionBox");
const optionBuffer = document.getElementById("optionBuffer");
const answerBuffer = document.getElementById("answerBuffer");
const remarkBox = document.getElementById("remarkBox");
const hrLine = document.getElementById("hrLine");
const newAns = document.getElementById("newAns");
const origAns = document.getElementById("origAns");
const classifyText = document.getElementById("classifyText");
const delimiter = "@---#*#*#*#*#*---@";

/* option */
for(let i = 0; i !== optionBuffer.children.length; ++i) {
  const span = document.createElement("span");
  span.innerText = delimiter;
  optionBuffer.children[i].prepend(span);
}

const optionExp = /^\s*([a-zA-Z]\s*[ \.]\s*)?(.+?)\s*$/;
const alphabetExp = /^[a-zA-Z]$/;
const optionList = optionBuffer.innerText.split(delimiter);
const choiceList = [];

if(optionList.length >= 26) {
  alert("Too many choices！");
  throw "Too many options.";
}
for(let i = 0; i !== optionList.length; ++i) {
  const x = optionList[i];
  optionList[i] = optionExp.exec(x)[2];
  choiceList.push(String.fromCharCode(65 + i));
}

pseudo_shuffle_inplace(optionList);
pseudo_shuffle_inplace(choiceList);

/* answer */
const answerList = Array.from(answerBuffer.innerText.trim()).filter(x => alphabetExp.exec(x) !== null);
if(answerList.length === 0 || answerList.length > choiceList.length) {
  alert("Invalid Answer！");
  throw "Invalid answer.";
}
for(let i = 0; i !== answerList.length; ++i) {
  const x = answerList[i];
  answerList[i] = x.trim().toUpperCase();
}

/* render */
const is_single = (answerList.length === 1);
const chosenList = [];
const liList = [];
classifyText.innerText = is_single ? "Single Choice" : "Multiple Choices";
for(let ii = 0; ii !== optionList.length; ++ii) {
  const i = ii + 0;
  chosenList.push(false);
  
  const checkbox_id = "checkbox-" + i;
  const li = document.createElement("li");
  liList.push(li);
  
  const check = document.createElement("input");
  check.type = is_single ? "radio" : "checkbox";
  check.id = checkbox_id;
  if(is_single)
    check.name = "checkbox-group";
  check.onchange = function() {
    if(is_single) {
      for(let j = 0; j !== chosenList.length; ++j)
        chosenList[j] = false;
    }
    chosenList[i] = this.checked;
  };
  
  const label = document.createElement("label");
  label.htmlFor = checkbox_id;
  label.innerText = optionList[i];
  
  li.appendChild(check);
  li.appendChild(label);
  
  optionBox.appendChild(li);
}

origAns.innerText = answerList.join("、");
const newAnswerList = [];
for(let i = 0; i !== answerList.length; ++i) {
  const ansIndex = choiceList.indexOf(answerList[i]);
  newAnswerList.push(String.fromCharCode(65 + ansIndex));
}
newAns.innerText = newAnswerList.join("、");

function onSubmit() {
  for(let i = 0; i !== chosenList.length; ++i) {
    const is_chosen = chosenList[i];
    const raw_choice = choiceList[i];
    const li = liList[i];
    const is_answer = (answerList.indexOf(raw_choice) !== -1);
    if(is_answer && is_chosen)
      li.className = "VeryRight";
    else if(is_answer && !is_chosen)
      li.className = "RightNotSelected";
    else if(!is_answer && is_chosen)
      li.className = "WrongSelected";
    else
      li.className = "";
  }
  hrLine.style = "";
  answerBox.style = "";
  remarkBox.style = "";
}
submitButton.onclick = onSubmit;

})();
</script>
"""

BACK = r"""<!--tuxzz.20201115.v0.r0-->
<div id="classifyBox" class="classify"><span id="classifyText"></span><span>：</span></div>
<div id="questionBox" class="text">{{Question}}</div>

{{#Options}}
<ol id="optionBox"></ol>
<div id="optionBuffer" style="display:none">{{Options}}</div>
<div id="answerBuffer" style="display:none">{{text:Answer}}</div>
<hr id="hrLine" style="display:none">
<div id="answerBox" style="display:none">Answer：<span id="newAns"></span>（Original Answer:<span id="origAns"></span>）</div>
<div id="remarkBox" style="display:none">Remark：{{Remark}}</div>
<button id="submitButton">Submit</button>
{{/Options}}


<script>
(function() {
"use strict";

const date = new Date();
function pseudo_shuffle_inplace(array) {
		let seed = date.getDay() * 60 + date.getMinutes();
    let currentIndex = array.length, temporaryValue, randomIndex;
    seed = seed || 1;
    let random = function() {
      var x = Math.sin(seed++) * 10000;
      return x - Math.floor(x);
    };
    // While there remain elements to shuffle...
    while (0 !== currentIndex) {
      // Pick a remaining element...
      randomIndex = Math.floor(random() * currentIndex);
      currentIndex -= 1;
      // And swap it with the current element.
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }
    return array;
}

const optionBox = document.getElementById("optionBox");
const optionBuffer = document.getElementById("optionBuffer");
const answerBuffer = document.getElementById("answerBuffer");
const remarkBox = document.getElementById("remarkBox");
const hrLine = document.getElementById("hrLine");
const newAns = document.getElementById("newAns");
const origAns = document.getElementById("origAns");
const classifyText = document.getElementById("classifyText");
const delimiter = "@---#*#*#*#*#*---@";

/* option */
for(let i = 0; i !== optionBuffer.children.length; ++i) {
  const span = document.createElement("span");
  span.innerText = delimiter;
  optionBuffer.children[i].prepend(span);
}

const optionExp = /^\s*([a-zA-Z]\s*[ \.]\s*)?(.+?)\s*$/;
const alphabetExp = /^[a-zA-Z]$/;
const optionList = optionBuffer.innerText.split(delimiter);
const choiceList = [];

if(optionList.length >= 26) {
  alert("Too many choices！");
  throw "Too many options.";
}
for(let i = 0; i !== optionList.length; ++i) {
  const x = optionList[i];
  optionList[i] = optionExp.exec(x)[2];
  choiceList.push(String.fromCharCode(65 + i));
}

pseudo_shuffle_inplace(optionList);
pseudo_shuffle_inplace(choiceList);

/* answer */
const answerList = Array.from(answerBuffer.innerText.trim()).filter(x => alphabetExp.exec(x) !== null);
if(answerList.length === 0 || answerList.length > choiceList.length) {
  alert("Invalid answer！");
  throw "Invalid answer.";
}
for(let i = 0; i !== answerList.length; ++i) {
  const x = answerList[i];
  answerList[i] = x.trim().toUpperCase();
}

/* render */
const is_single = (answerList.length === 1);
const chosenList = [];
const liList = [];
classifyText.innerText = is_single ? "Single Choice" : "Multiple Choices";
for(let ii = 0; ii !== optionList.length; ++ii) {
  const i = ii + 0;
  chosenList.push(false);
  
  const checkbox_id = "checkbox-" + i;
  const li = document.createElement("li");
  liList.push(li);
  
  const check = document.createElement("input");
  check.type = is_single ? "radio" : "checkbox";
  check.id = checkbox_id;
  if(is_single)
    check.name = "checkbox-group";
  check.onchange = function() {
    if(is_single) {
      for(let j = 0; j !== chosenList.length; ++j)
        chosenList[j] = false;
    }
    chosenList[i] = this.checked;
  };
  
  const label = document.createElement("label");
  label.htmlFor = checkbox_id;
  label.innerText = optionList[i];
  
  li.appendChild(check);
  li.appendChild(label);
  
  optionBox.appendChild(li);
}

origAns.innerText = answerList.join("、");
const newAnswerList = [];
for(let i = 0; i !== answerList.length; ++i) {
  const ansIndex = choiceList.indexOf(answerList[i]);
  newAnswerList.push(String.fromCharCode(65 + ansIndex));
}
newAns.innerText = newAnswerList.join("、");

function onSubmit() {
  for(let i = 0; i !== chosenList.length; ++i) {
    const is_chosen = chosenList[i];
    const raw_choice = choiceList[i];
    const li = liList[i];
    const is_answer = (answerList.indexOf(raw_choice) !== -1);
    if(is_answer && is_chosen)
      li.className = "VeryRight";
    else if(is_answer && !is_chosen)
      li.className = "RightNotSelected";
    else if(!is_answer && is_chosen)
      li.className = "WrongSelected";
    else
      li.className = "";
  }
  hrLine.style = "";
  answerBox.style = "";
  remarkBox.style = "";
}
submitButton.onclick = onSubmit;
onSubmit()
})();
</script>
"""

CSS = """<style>
.card {
  font-family: sans;
}
.card {
  font-family: sans;
  font-size: 17px;
  text-align: center;
  color: white;
  background-color: #272822;
}
ul {
display: inline-block;
text-align: left;
}
ol {
display: inline-block;
text-align: left;
}
div {
  margin: 5px auto;
}
.text {
  color: #e6db74;
  text-align: center;
}
.classify {
  font-size: 22px;
}
.remark {
  margin-top: 15px;
  font-size: 16px;
  color: #eeeebb;
  text-align: center;
}
.cloze {
  font-weight: bold;
  color: #a6e22e;
  display: inline;
  margin-right: 15px;
}
#optionBox {
  list-style: upper-latin;
}
#optionBox label, #optionBox input {
  cursor: pointer;
}
#optionBox li:hover {
  color: #eeeebb;
}
#optionBox li {
  margin-top: 10px;
}
#optionBox li.VeryRight {
  color: green;
}
#optionBox li.RightNotSelected {
  color: green;
  text-decoration: underline;
}
#optionBox li.WrongSelected {
  color: red;
  text-decoration: line-through;
}
#performance {
  text-align: center;
  font-size: 12px;
  margin-top: 0px;
  color: #eeeebb;
}
</style>
"""

MODELNAME = "AnkiLink-Choices"
MODELID = 1145141919

_model = Model(
    modelId=MODELID,
    modelName=MODELNAME,
    fields=["Question", "Options", "Answer", "Remark"],
    templates=[
        {
            "Name": "Card 1",
            "Front": FRONT,
            "Back": BACK
        }
    ],
    css=CSS
)


class ChoicesNote(Note):
    def __init__(self, question, options, answer, remark, deck="Export", tags=("#Export",)):
        global _model
        super().__init__(model=_model, fields={
            "Question": question, "Options": options, "Answer": answer, "Remark": remark},
            deck=deck, tags=tags)
