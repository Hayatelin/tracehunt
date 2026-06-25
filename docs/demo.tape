# TraceHunt demo recording (VHS by charmbracelet)
# 1) Install VHS:  https://github.com/charmbracelet/vhs   (e.g. `brew install vhs` or `winget install charmbracelet.vhs`)
# 2) From the repo root, run:   vhs docs/demo.tape
# 3) It writes docs/demo.gif. Then change the README image to docs/demo.gif.
Output docs/demo.gif
Set FontSize 18
Set Width 1100
Set Height 640
Set Theme "Dracula"
Set Padding 18
Set TypingSpeed 45ms

Type "tracehunt johndoe --summary --html johndoe.html"
Sleep 600ms
Enter
Sleep 4s
Type "open johndoe.html   # a shareable, styled report"
Sleep 800ms
Enter
Sleep 2s
