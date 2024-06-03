import {
  UnitDefault,
  UnitOpenAnswer,
  UnitMultipleChoice,
  UnitPairing,
} from "#components"

export default function () {
  return (type: UnitType) =>
    ({
      default: UnitDefault,
      open_answer: UnitOpenAnswer,
      multiple_choice: UnitMultipleChoice,
      pairing: UnitPairing,
    })[type]
}
