// Sep 24, 2025
// Jan 30, 2026 no need to unzip files
// v3.2
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

	"github.com/dablelv/cyan/zip"
)

var (
	files []string
	pns   = []string{"3", "4", "5", "9", "11", "14", "16", "17"}
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
	length := len(device)
	num := string([]rune(device)[11:14])
	maj := string([]rune(device)[length-6 : length-3])
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

func getCont(fname string, sep rune, devi, tmpri, tmprc int) {
	cont := readFile(fname, sep)
	for _, line := range cont {
		var want [3]string
		want[0] = line[devi]
		want[1] = line[tmpri]
		want[2] = line[tmprc]
		addInto(want)
	}
}

func readFile(fl string, sep rune) [][]string {
	file, _ := os.Open(fl)
	defer file.Close()

	obj := csv.NewReader(file)
	obj.Comma = sep

	var sli [][]string
	for {
		record, err := obj.Read()
		if err == io.EOF {
			break
		}
		sli = append(sli, record)
	}
	return sli[1:]
}

func countAll() {
	for _, file := range files {
		switch true {
		case strings.HasSuffix(file, "runlog"):
			getCont(file, '|', 0, 1, 2)
		case strings.HasSuffix(file, "csv"):
			getCont(file, ',', 3, 5, 4)
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

func fmtPm(pn string) (pm string) {
	intpn, _ := strconv.Atoi(pn)
	fpn := fmt.Sprintf("%02d", intpn)
	pm = fmt.Sprintf("%sA-SRV/%sA-DBS", fpn, fpn)
	return
}

func display() {
	fmt.Printf("               \t\t%s\t\t%s\n", "INPUT_TEMP", "CPU_TEMP")
	border := strings.Repeat("=", 63)
	green := "\033[32m%s\033[0m"
	fmt.Printf(green+"\n", border)

	for _, pn := range pns {
		pm := fmtPm(pn)
		oneline := fmt.Sprintf("%s\t\t%s/%s\t\t%s/%s", pm, getVal(pm[:7], 0), getVal(pm[8:], 0), getVal(pm[:7], 2), getVal(pm[8:], 2))
		fmt.Println(oneline)
	}
	fmt.Printf(green+"\n", border)
	for _, fname := range files {
		fmt.Printf(green+" %s\n", "calculated:",fname)
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

func unzipFiles() {
	currentTime := time.Now()
	fmtime := currentTime.Format("20060102")
	patternz := fmt.Sprintf("*%s*.zip", fmtime)
	zfiles, _ := filepath.Glob(patternz)
	for _, zfile := range zfiles {
		dirname := strings.Replace(zfile, ".zip", "", -1)
		zip.Unzip(zfile, dirname)
		patn := fmt.Sprintf("%s/*[0-9].csv", dirname)
		csvname := dirname + ".csv"
		files, _ := filepath.Glob(patn)
		os.Rename(files[0], csvname)
		os.RemoveAll(dirname)
		os.Remove(zfile)
	}
}

func fileExist(fl string) bool {
	if _, err := os.Stat(fl); err == nil {
		return true
	} else {
		return false
	}
}

func getPns() {
	if fileExist("config") {
		pns = readFile("config", ',')[0]
	}
}

func main() {
	unzipFiles()
	getFiles()
	getPns()
	countAll()
	mvFiles()
	display()
}
