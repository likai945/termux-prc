// Sep 24, 2025
// v2.5
// by LiKai

package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
	"time"
)

var (
	files []string
	res   = make(map[string][4]float64)
)

func getFiles() {
	currentTime := time.Now()
	cstSh, err := time.LoadLocation("Asia/Shanghai")
	if err == nil {
		currentTime = currentTime.In(cstSh)
	}
	fmtime := currentTime.Format("20060102")

	patternr := fmt.Sprintf("%s_*.runlog", fmtime)
	patternc := fmt.Sprintf("*%s*.csv", fmtime)
	rfiles, _ := filepath.Glob(patternr)
	cfiles, _ := filepath.Glob(patternc)
	files = append(cfiles, rfiles...)

	if len(files) == 0 {
		fmt.Println("未找到今日温度文件，请检查。")
		forWin()
		os.Exit(2)
	}
}

func addInto(info [3]string) {
	device := info[0]
	temprcpu := info[2]
	temprinp := info[1]
	num := string([]rune(device)[11:14])
	maj := string([]rune(device)[27:30])
	pool := num + "-" + maj

	forval := res[pool]
	fltemprinp, err := strconv.ParseFloat(temprinp, 64)
	if err == nil {
		forval[0]++
		forval[1] += fltemprinp
	}

	fltemprcpu, err := strconv.ParseFloat(temprcpu, 64)
	if err == nil {
		forval[2]++
		forval[3] += fltemprcpu
		res[pool] = forval
	}
}

func readFile(fname string, sep rune, devi, tmpri, tmprc int) {
	file, _ := os.Open(fname)
	defer file.Close()

	obj := csv.NewReader(file)
	obj.Comma = sep

	for line := 0; ; line++ {
		record, err := obj.Read()
		if err == io.EOF {
			break
		}
		var want [3]string
		want[0] = record[devi]
		want[1] = record[tmpri]
		want[2] = record[tmprc]
		if line > 0 {
			addInto(want)
		}
	}
}

func countAll() {
	for _, file := range files {
		switch true {
		case strings.HasSuffix(file, "runlog"):
			readFile(file, '|', 0, 1, 2)
		case strings.HasSuffix(file, "csv"):
			readFile(file, ',', 3, 5, 4)
		}
	}
}

func getVal(key string, s int) string {
	val, exis := res[key]
	if exis == true {
		disptmp := val[1+s] / val[0+s]
		return fmt.Sprintf("%.2f°C", disptmp)
	} else {
		return "NO_DATA"
	}
}

func forWin() {
	if strings.EqualFold(runtime.GOOS, "windows") {
		fmt.Scanf("keep on")
	}
}

func display() {
	border := strings.Repeat("=", 63)
	fmt.Printf("               \t\t%s\t\t%s", "INPUT_TEMP", "CPU_TEMP")
	fmt.Printf("\n\033[32m%s\033[0m\n", border)
	fmt.Printf("03A-SRV/03A-DBS\t\t%s/%s\t\t%s/%s\n", getVal("03A-SRV", 0), getVal("03A-DBS", 0), getVal("03A-SRV", 2), getVal("03A-DBS", 2))
	fmt.Printf("04A-SRV/04A-DBS\t\t%s/%s\t\t%s/%s\n", getVal("04A-SRV", 0), getVal("04A-DBS", 0), getVal("04A-SRV", 2), getVal("04A-DBS", 2))
	fmt.Printf("05A-SRV/05A-DBS\t\t%s/%s\t\t%s/%s\n", getVal("05A-SRV", 0), getVal("05A-DBS", 0), getVal("05A-SRV", 2), getVal("05A-DBS", 2))
	fmt.Printf("09A-SRV/09A-DBS\t\t%s/%s\t\t%s/%s\n", getVal("09A-SRV", 0), getVal("09A-DBS", 0), getVal("09A-SRV", 2), getVal("09A-DBS", 2))
	fmt.Printf("11A-SRV/11A-DBS\t\t%s/%s\t\t%s/%s\n", getVal("11A-HSR", 0), getVal("11A-DBS", 0), getVal("11A-HSR", 2), getVal("11A-DBS", 2))
	fmt.Printf("14A-SRV/14A-DBS\t\t%s/%s\t\t%s/%s\n", getVal("14A-HSR", 0), getVal("14A-DBS", 0), getVal("14A-HSR", 2), getVal("14A-DBS", 2))
	fmt.Printf("16A-SRV/16A-DBS\t\t%s/%s\t\t%s/%s\n", getVal("16A-HSR", 0), getVal("16A-DBS", 0), getVal("16A-HSR", 2), getVal("16A-DBS", 2))
	fmt.Printf("17A-SRV/17A-DBS\t\t%s/%s\t\t%s/%s\n", getVal("17A-HSR", 0), getVal("17A-DBS", 0), getVal("17A-HSR", 2), getVal("17A-DBS", 2))
	fmt.Printf("\033[32m%s\033[0m\n\n", border)
	for _, fname := range files {
		fmt.Printf("\033[32mcalculated:\033[0m %s\n", fname)
	}
	fmt.Println()
	forWin()
}

func mvFiles() {
	os.Mkdir("calculated", 0o755)
	for _, file := range files {
		newpath := fmt.Sprintf("calculated/%s", file)
		os.Rename(file, newpath)
	}
}

func main() {
	getFiles()
	countAll()
	mvFiles()
	display()
}
