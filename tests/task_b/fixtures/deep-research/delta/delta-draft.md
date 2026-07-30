# Delta result

The verifier now returns a failing verdict and non-zero exit for an invented URL
[1]. This closes the previous fail-open behavior for structural issues.

## Limitations

The delta validates local mapping only. It does not establish public URL
reachability.

## References

[1] Source A, https://nist.gov/fixture/citation-contract
