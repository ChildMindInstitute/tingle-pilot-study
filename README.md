# tingle-pilot-study
Pilot study for [Tingle wrist-worn position-tracking device](https://matter.childmind.org/tingle) intended for use with body-focused repetitive behaviors such as trichotillomania.

[![CircleCI](https://circleci.com/gh/ChildMindInstitute/tingle-pilot-study/tree/master.svg?style=shield&circle-token=7650679b4d1aa3526b523d32fe49526b8cf5a180)](https://circleci.com/gh/ChildMindInstitute/tingle-pilot-study/tree/master)

🐍 ![Python coverage](.circleci/coverage.svg)

☕ 68.42% JavaScript coverage

<!--ts-->
   * [tingle-pilot-study](#tingle-pilot-study)
      * [Highlighted Functions](#highlighted-functions)
         * [data.dataloader.count_ontarget_samples](#datadataloadercount_ontarget_samples)
         * [data.dataloader.update_too_few](#datadataloaderupdate_too_few)
      * [Data Dictionary](#data-dictionary)
         * [firstCoordinator](#firstcoordinator)
         * [secondCoordinator](#secondcoordinator)
         * [coordinator1](#coordinator1)
         * [coordinator2](#coordinator2)
         * [distance](#distance)
         * [hand](#hand)
         * [human-readable timestamp](#human-readable-timestamp)
         * [notes](#notes)
         * [ontarget](#ontarget)
         * [participant](#participant)
         * [pitch](#pitch)
         * [question](#question)
         * [roll](#roll)
         * [section](#section)
         * [step](#step)
         * [step_c2](#step_c2)
         * [target](#target)
         * [thermopile1](#thermopile1)
         * [thermopile2](#thermopile2)
         * [thermopile3](#thermopile3)
         * [thermopile4](#thermopile4)
         * [timestamp](#timestamp)
         * [username](#username)

<!-- Added by: jclucas, at: 2018-05-17T14:14-04:00 -->

<!--te-->

## Highlighted Functions

### data.dataloader.count_ontarget_samples
Function to count usable samples. Returns a(n optionally human-readable, ie with labeled steps) pandas DataFrame of ontarget samples per step per participant. [📚 documentation](http://tingle-pilot-study.readthedocs.io/en/latest/data.html?#data.dataloader.count_ontarget_samples)

### data.dataloader.update_too_few
Function to update a DataFrame with an inappropriate number of samples in coordinator agreement. Returns a pandas DataFrame updated with single-rater matches  replacing dual-rater agreement in cases indicated by condition given. [📚 documentation](http://tingle-pilot-study.readthedocs.io/en/latest/data.html?#data.dataloader.update_too_few)

## Data Dictionary
### firstCoordinator
*string* name of coordinator giving instructions, facing the participant's face, and recording data via [Tingle Gesture Detection Pilot Study App](https://okgab.com/tinglemin/) connected to the Tingle via Bluetooth
### secondCoordinator
*string* name of coordinator not giving instructions, facing the participant's right side, and recording data via [Tingle Gesture Detection Pilot Study App](https://matter.childmind.org/tingle/tingle-min2.html) not connected to the Tingle
### coordinator1
*boolean* if the Tingle was proximal to the [target](#target) per [firstCoordinator](#firstcoordinator)
### coordinator2
*boolean* if the Tingle was proximal to the [target](#target) per [secondCoordinator](#secondcoordinator)
### distance
*numeric* output of proximity sensor
### hand
*string* hand on which the Tingle was worn, 'L' for left, 'R' for right
### human-readable timestamp
*datetime* [timestamp](#timestamp) converted to [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)
### notes
*string* notes entered by either coordinator in his respective Tingle Gesture Detection Pilot Study App
### ontarget
*boolean* coordinator-agreed proximity to [target](#target) calculated as \[([coordinator1](#coordinator1) & [coordinator2](#coordinator2)) if ([step](#step) = [step_c2](#step_c2))\]
### participant
*int* index of participant, incrementing with each reset of the pair of Tingle Gesture Detection Pilot Study Apps. Indexed [participant](#participant)s with no true values in [ontarget](#ontarget) are indications of asynchronous resets between coordinators and not actual participants.
### pitch
*numeric* caluclated from accelerometer output
### question
*string* text of the prompt given by a coordinator prior to the current action
### roll
*numeric* caluclated from accelerometer output
### section
*string* 'A', 'B', 'C' or 'D' indicating semantic groupings of [question](#question)s
### step
*integer* sequential index of [question](#question) per [firstCoordinator](#firstcoordinator)
### step_c2
*integer* sequential index of [question](#question) per [secondCoordinator](#secondcoordinator)
### target
*string* the [target](#target) for which coordinators would indicate proximity
### thermopile1
*numeric* output of one thermopile
### thermopile2
*numeric* output of one thermopile
### thermopile3
*numeric* output of one thermopile
### thermopile4
*numeric* output of one thermopile
### timestamp
*integer* [Unix time](https://en.wikipedia.org/wiki/Unix_time) milliseconds
### username
*string* name of coordinator who added that row's [notes](#notes)
