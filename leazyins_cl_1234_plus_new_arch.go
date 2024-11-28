//Nov 27, 2024
//v2.0
//by LiKai

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

var files []string
var res = make(map[string][2]float64)

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

func addInto(info [2]string) {
	device := info[0]
	tempr := info[1]
	num := string([]rune(device)[11:14])
	maj := string([]rune(device)[27:30])
	pool := num + "-" + maj
	fltempr, err := strconv.ParseFloat(tempr, 64)

	if err == nil {
		thisi := res[pool]
		thisi[0]++
		thisi[1] += fltempr
		res[pool] = thisi
	}
}

func readFile(fname string, sep rune, devi, tmpr int) {
	file, _ := os.Open(fname)
	defer file.Close()

	obj := csv.NewReader(file)
	obj.Comma = sep

	for line := 0; ; line++ {
		record, err := obj.Read()
		if err == io.EOF {
			break
		}
		var want [2]string
		want[0] = record[devi]
		want[1] = record[tmpr]
		if line > 0 {
			addInto(want)
		}
	}
}

func countAll() {
	for _, file := range files {
		switch true {
		case strings.HasSuffix(file, "runlog"):
			readFile(file, '|', 0, 2)
		case strings.HasSuffix(file, "csv"):
			readFile(file, ',', 3, 4)
		}
	}
}

func getVal(key string) string {
	val, exis := res[key]
	if exis == true {
		disptmp:=val[1]/val[0]
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

func display(){
	border := strings.Repeat("=", 39)
	fmt.Printf("\n\033[32m%s\033[0m\n", border)
	fmt.Printf("03A-SRV/03A-DBS\t\t%s/%s\n", getVal("03A-SRV"), getVal("03A-DBS"))
	fmt.Printf("04A-SRV/04A-DBS\t\t%s/%s\n", getVal("04A-SRV"), getVal("04A-DBS"))
	fmt.Printf("05A-SRV/05A-DBS\t\t%s/%s\n", getVal("05A-SRV"), getVal("05A-DBS"))
	fmt.Printf("09A-SRV/09A-DBS\t\t%s/%s\n", getVal("09A-SRV"), getVal("09A-DBS"))
	fmt.Printf("11A-SRV/11A-DBS\t\t%s/%s\n", getVal("11A-HSR"), getVal("11A-DBS"))
	fmt.Printf("\033[32m%s\033[0m\n\n", border)
	for _, fname := range files {
		fmt.Printf("\033[32mcalculated:\033[0m %s\n", fname)
	}
	fmt.Println()
}

func main() {
	getFiles()
	countAll()
	display()
	forWin()
}
