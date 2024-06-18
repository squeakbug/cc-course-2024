use std::process::{Command, Stdio};
use assert_cmd::{cargo::CargoError, prelude::*};
use predicates::{constant, prelude::*};

#[test]
fn it_works() {
    assert_eq!(2, 2);
}
