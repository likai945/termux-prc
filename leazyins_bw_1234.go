//Oct 27, 2024
//by LiKai

package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strconv"
	"time"
)

func getFile() string {
	currentTime := time.Now()
	fmtime := currentTime.Format("20060102")
	pattern := fmt.Sprintf("%s_*.runlog", fmtime)
	files, _ := filepath.Glob(pattern)
	if len(files) == 0 {
		fmt.Println("no todays runlog files")
		os.Exit(2)
	}
	return files[0]
}

func readFile() [][]string {
	fname := getFile()
	fmt.Printf("\ncalculated %s\n", fname)
	file, _ := os.Open(fname)
	defer file.Close()

	obj := csv.NewReader(file)
	obj.Comma = '|'

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

func trsDic() map[string][]int {
	fobj := readFile()
	res := map[string][]int{}
	for _, i := range fobj {
		device := i[0]
		tempr := i[2]

		num := string([]rune(device)[11:14])
		maj := string([]rune(device)[27:30])
		pool := num + "-" + maj
		g_tempr, err := strconv.Atoi(tempr)

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

func compAvg(sli []int) float64 {
	var sum int = 0
	for _, i := range sli {
		sum += i
	}
	addend := len(sli)
	avg := float64(sum) / float64(addend)
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
		return "no_data"
	}
}

func main() {
	res := compute()
	fmt.Printf("\n===============\n")
	fmt.Printf("03A-SRV/03A-DBS\t\t%s/%s\n", checkExis(res, "03A-SRV"), checkExis(res, "03A-DBS"))
	fmt.Printf("04A-SRV/04A-DBS\t\t%s/%s\n", checkExis(res, "04A-SRV"), checkExis(res, "04A-DBS"))
	fmt.Printf("05A-SRV/05A-DBS\t\t%s/%s\n", checkExis(res, "05A-SRV"), checkExis(res, "05A-DBS"))
	fmt.Printf("09A-SRV/09A-DBS\t\t%s/%s\n", checkExis(res, "09A-SRV"), checkExis(res, "09A-DBS"))
	fmt.Printf("11A-SRV/11A-DBS\t\t%s/%s\n", checkExis(res, "11A-HSR"), checkExis(res, "11A-DBS"))
	fmt.Printf("===============\n\n")

}
