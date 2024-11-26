//Nov 26, 2024
//v1.2
//by LiKai

package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"
)

var fnames []string

func getFiles() []string {
	currentTime := time.Now()
	cstSh, _ := time.LoadLocation("Asia/Shanghai")
	fmtime := currentTime.In(cstSh).Format("20060102")

	patternr := fmt.Sprintf("%s_*.runlog", fmtime)
	patternc := fmt.Sprintf("*%s*.csv", fmtime)
	rfiles, _ := filepath.Glob(patternr)
	cfiles, _ := filepath.Glob(patternc)
	files := append(cfiles, rfiles...)

	if len(files) == 0 {
		fmt.Println("未找到温度文件，请检查。")
		os.Exit(2)
	}
	return files
}

func readFile(fname string, sep rune, devi, tmpr int) [][]string {
	file, _ := os.Open(fname)
	defer file.Close()

	obj := csv.NewReader(file)
	obj.Comma = sep

	var sli [][]string
	for {
		record, err := obj.Read()
		if err == io.EOF {
			break
		}
		var want [2]string
		want[0] = record[devi]
		want[1] = record[tmpr]
		wantsli := want[:]
		sli = append(sli, wantsli)
	}
	return sli[1:]
}

func toSlice() [][]string {
	fnames = getFiles()
	var sli [][]string
	for _, file := range fnames {
		switch true {
		case strings.HasSuffix(file, "runlog"):
			slipiece := readFile(file, '|', 0, 2)
			sli = append(sli, slipiece...)
		case strings.HasSuffix(file, "csv"):
			slipiece := readFile(file, ',', 3, 4)
			sli = append(sli, slipiece...)
		}
	}
	return sli
}

func trsDic() map[string][]float64 {
	fobj := toSlice()
	res := map[string][]float64{}
	for _, i := range fobj {
		device := i[0]
		tempr := i[1]

		num := string([]rune(device)[11:14])
		maj := string([]rune(device)[27:30])
		pool := num + "-" + maj
		g_tempr, err := strconv.ParseFloat(tempr, 64)

		if err != nil {
			continue
		} else {
			tmp := res[pool]
			tmp = append(tmp, g_tempr)
			res[pool] = tmp
		}
	}
	return res
}

func compAvg(sli []float64) float64 {
	var sum float64 = 0
	for _, i := range sli {
		sum += i
	}
	addend := len(sli)
	avg := sum / float64(addend)
	return avg
}

func compute() map[string]float64 {
	dict := trsDic()
	computed := map[string]float64{}
	for key, val := range dict {
		avg := compAvg(val)
		computed[key] = avg
	}
	return computed
}

func checkExis(res map[string]float64, key string) string {
	val, exis := res[key]
	if exis == true {
		return fmt.Sprintf("%.2f°C", val)
	} else {
		return "NO_DATA"
	}
}

func main() {
	res := compute()
	border := strings.Repeat("=", 39)
	fmt.Printf("\n\033[32m%s\033[0m\n", border)
	fmt.Printf("03A-SRV/03A-DBS\t\t%s/%s\n", checkExis(res, "03A-SRV"), checkExis(res, "03A-DBS"))
	fmt.Printf("04A-SRV/04A-DBS\t\t%s/%s\n", checkExis(res, "04A-SRV"), checkExis(res, "04A-DBS"))
	fmt.Printf("05A-SRV/05A-DBS\t\t%s/%s\n", checkExis(res, "05A-SRV"), checkExis(res, "05A-DBS"))
	fmt.Printf("09A-SRV/09A-DBS\t\t%s/%s\n", checkExis(res, "09A-SRV"), checkExis(res, "09A-DBS"))
	fmt.Printf("11A-SRV/11A-DBS\t\t%s/%s\n", checkExis(res, "11A-HSR"), checkExis(res, "11A-DBS"))
	fmt.Printf("\033[32m%s\033[0m\n\n", border)
	for _, fname := range fnames {
		fmt.Printf("\033[32mcalculated:\033[0m %s\n", fname)
	}
	fmt.Println()
}
