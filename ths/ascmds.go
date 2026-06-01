package ths

import (
	"fmt"
	"os/exec"
	"strings"
)

func Run(script string) (string, error) {
	cmd := exec.Command("/usr/bin/osascript", "-e", script)
	output, err := cmd.Output()
	if err != nil {
		if exitErr, ok := err.(*exec.ExitError); ok {
			return strings.TrimSpace(string(exitErr.Stderr)), fmt.Errorf("osascript error: %w", exitErr)
		}
		return "", err
	}
	return strings.TrimSpace(string(output)), nil
}
