#!/usr/bin/env bash
set -u
set -o pipefail

ROOT_DIR="${ROOT_DIR:-materials/logistics/alpha}"
VALIDATE_BIN="${VALIDATE_BIN:-validate}"
VARIANTS=(plan_front plan_scatter)

if ! command -v "$VALIDATE_BIN" >/dev/null 2>&1; then
  echo "ERROR: VAL validator not found: $VALIDATE_BIN" >&2
  echo "Set VALIDATE_BIN=/path/to/validate or put validate on PATH." >&2
  exit 127
fi

if [[ ! -d "$ROOT_DIR" ]]; then
  echo "ERROR: missing root directory: $ROOT_DIR" >&2
  exit 2
fi

total=0
valid=0
invalid=0
missing=0

shopt -s nullglob

for problem_dir in "$ROOT_DIR"/p*; do
  [[ -d "$problem_dir" ]] || continue

  problem_id="$(basename "$problem_dir")"
  problem_path="$problem_dir/$problem_id.pddl"
  plan_path="$problem_dir/$problem_id.plan"

  if [[ ! -f "$problem_path" ]]; then
    echo "MISSING problem file: $problem_path"
    missing=$((missing + 1))
    continue
  fi

  if [[ ! -f "$plan_path" ]]; then
    echo "MISSING plan file: $plan_path"
    missing=$((missing + 1))
    continue
  fi

  for variant in "${VARIANTS[@]}"; do
    variant_dir="$problem_dir/$variant"
    domain_path="$variant_dir/domain.pddl"

    if [[ ! -f "$domain_path" ]]; then
      echo "MISSING domain file: $domain_path"
      missing=$((missing + 1))
      continue
    fi

    output_file="$(mktemp)"
    total=$((total + 1))

    if "$VALIDATE_BIN" -v "$domain_path" "$problem_path" "$plan_path" >"$output_file" 2>&1 \
      && grep -qi "Plan valid" "$output_file"; then
      echo "VALID   $problem_id $variant plan=$plan_path"
      valid=$((valid + 1))
    else
      echo "INVALID $problem_id $variant plan=$plan_path"
      sed 's/^/  /' "$output_file" | tail -n 20
      invalid=$((invalid + 1))
    fi

    rm -f "$output_file"
  done
done

echo
echo "Summary:"
echo "  checked: $total"
echo "  valid:   $valid"
echo "  invalid: $invalid"
echo "  missing: $missing"

if (( invalid > 0 || missing > 0 )); then
  exit 1
fi

exit 0
