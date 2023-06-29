graph [
  directed 1
  node [
    id 0
    label "generative"
  ]
  node [
    id 1
    label "Apache 2.0"
  ]
  node [
    id 2
    label "pycomposer"
  ]
  node [
    id 3
    label "GPL2"
  ]
  node [
    id 4
    label "pygan"
  ]
  node [
    id 5
    label "Python"
  ]
  node [
    id 6
    label "Unix Shell"
  ]
  edge [
    source 0
    target 1
    label "has_license"
  ]
  edge [
    source 0
    target 6
    label "used_language"
  ]
  edge [
    source 0
    target 5
    label "used_language"
  ]
  edge [
    source 2
    target 3
    label "has_license"
  ]
  edge [
    source 2
    target 5
    label "used_language"
  ]
  edge [
    source 4
    target 3
    label "has_license"
  ]
  edge [
    source 4
    target 5
    label "used_language"
  ]
]
