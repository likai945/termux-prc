//Nov 2, 2024
//by LiKai

package main

import (
	"encoding/csv"
	"fmt"
	"github.com/xuri/excelize/v2"
	"io"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
	"time"
)

var f = excelize.NewFile()
var smrr, hisr, crtr int
var totalmap = map[string]string{}
var currentTime = time.Now()
var date string = currentTime.Format("2006-01-02")
var namedate string = currentTime.Format("20060102")
var bookname string = fmt.Sprintf("附件1：告警分析-中兴资源池%s.xlsx", namedate)

func readFile(fl string) [][]string {
	file, _ := os.Open(fl)
	defer file.Close()

	obj := csv.NewReader(file)

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

func toDisc(file string, indx int) map[string][3][]string {
	alrmsli := readFile(file)
	amap := map[string][3][]string{}
	for _, row := range alrmsli {
		desc := row[indx]
		rowval := amap[desc]
		sttt := append(rowval[0], row[7])
		endt := append(rowval[1], row[9])
		devi := append(rowval[2], row[5]+"名="+row[6])
		amap[desc] = [3][]string{sttt, endt, devi}
	}
	return amap
}

func toWall(file string, indx int) [][]string {
	amap := toDisc(file, indx)
	resmap := toDict()
	var sum int
	var lines [][]string
	for key, val := range amap {
		desc := key
		sttt := strings.Join(val[0], "\n")
		endt := strings.Join(val[1], "\n")
		devi := strings.Join(val[2], "\n")
		nu := len(val[2])
		sum += nu
		num := strconv.Itoa(nu)
		res := resmap[desc]
		var line []string
		if indx == 3 {
			line = []string{sttt, endt, devi, desc, num, res, "是"}
		} else if indx == 4 {
			line = []string{sttt, endt, devi, desc, num, res}
		}
		lines = append(lines, line)
	}
	totalmap[file] = strconv.Itoa(sum)
	return lines
}

func writeFrm(sheet string, line []string) {
	for fld, cell := range line {
		field := int(rune('A')) + fld
		cellcrd := string(field) + "1"
		f.SetCellValue(sheet, cellcrd, cell)
	}
}

func before() {
	defer func() {
		if err := f.Close(); err != nil {
			fmt.Println(err)
		}
	}()
	f.NewSheet("Sheet2")
	f.NewSheet("Sheet3")

	smrtitle := []string{"时间", "资源池", "历史告警数", "当前告警数量", "当前告警清除数量", "当前告警剩余"}
	histitle := []string{"时间", "资源池", "告警时间", "清除时间", "对象名称", "告警描述", "数量", "处理结果"}
	crttitle := []string{"时间", "资源池", "告警时间", "确认恢复时间", "对象名称", "告警描述", "数量", "处理结果", "是否清除", "未确认恢复原因"}

	writeFrm("Sheet1", smrtitle)
	writeFrm("Sheet2", histitle)
	writeFrm("Sheet3", crttitle)

	smrr++
	hisr++
	crtr++
}

func isNumberic(str string) bool {
	_, err := strconv.Atoi(str)
	return err == nil
}

func writeSheet(sheet, pool string, ruler int, lines [][]string) {
	poolst := "B" + strconv.Itoa(ruler+1)

	f.SetCellValue(sheet, "A2", date)
	f.SetCellValue(sheet, poolst, pool)

	for rownum, line := range lines {
		for fieldnum, cell := range line {
			field := int(rune('C')) + fieldnum
			row := strconv.Itoa(rownum + ruler + 1)
			cellcrd := string(field) + row
			datecrd := "A" + row
			poolcrd := "B" + row

			if isNumberic(cell) {
				numcell, _ := strconv.Atoi(cell)
				f.SetCellValue(sheet, cellcrd, numcell)
			} else {
				f.SetCellValue(sheet, cellcrd, cell)
			}

			f.MergeCell(sheet, "A2", datecrd)
			f.MergeCell(sheet, poolst, poolcrd)

			ruler, _ := strconv.Atoi(row)
			switch sheet {
			case "Sheet1":
				smrr = ruler
			case "Sheet2":
				hisr = ruler
			case "Sheet3":
				crtr = ruler
			}
		}
	}

}

func checkExist(file, pool string, hc int) [][]string {
	hcmap := map[int][][]string{
		4: [][]string{{"无告警，不涉及", "无告警，不涉及", "无告警，不涉及", "无告警，不涉及", "0", "无告警，不涉及"}},
		3: [][]string{{"无告警，不涉及", "无告警，不涉及", "无告警，不涉及", "无告警，不涉及", "0", "无告警，不涉及", "无告警，不涉及"}},
	}
	hcchmap := map[int]string{4: "历史", 3: "当前"}
	//magic num 4 is his, 3 is crt
	fexist, _ := filepath.Glob(file)
	var command string
	if len(fexist) == 0 {
		fmt.Printf("%s不存在,%s若无%s告警，请输入OK\n", file, pool, hcchmap[hc])
		fmt.Scanln(&command)
		if command == "ok" || command == "OK" {
			return hcmap[hc]
		} else {
			os.Exit(2)
		}
	}
	return toWall(file, hc)
}

func main() {
	before()
	pools := readFile("config")[0]
	for _, pool := range pools {
		re := regexp.MustCompile("[0-9]+")
		nums := re.FindAllString(pool, -1)
		cfile := fmt.Sprintf("c%s.csv", nums[0])
		hfile := fmt.Sprintf("h%s.csv", nums[0])
		writeSheet("Sheet2", pool, hisr, checkExist(hfile, pool, 4))
		writeSheet("Sheet3", pool, crtr, checkExist(cfile, pool, 3))
		writeSheet("Sheet1", pool, smrr, getKey(nums[0]))
	}
	after()
}

func toDict() map[string]string {
	resarr := readFile("result.csv")
	amap := map[string]string{}
	for _, val := range resarr {
		amap[val[0]] = val[1]
	}
	return amap
}

func after() {
	f.InsertRows("Sheet2", 1, 1)
	f.SetCellValue("Sheet2", "A1", "历史告警")
	f.MergeCell("Sheet2", "A1", "H1")
	f.InsertRows("Sheet3", 1, 1)
	f.SetCellValue("Sheet3", "A1", "当前告警")
	f.MergeCell("Sheet3", "A1", "J1")

	f.SetSheetName("Sheet1", "汇总")
	f.SetSheetName("Sheet2", "历史告警处理记录")
	f.SetSheetName("Sheet3", "当前告警处理记录")

	f.SaveAs(bookname)
}

func defaultKey(key, defkey string, anymap map[string]string) string {
	_, exist := anymap[key]
	if exist {
		return anymap[key]
	} else {
		return defkey
	}
}

func getKey(key string) [][]string {
	lines := [][]string{}
	hiscsv := fmt.Sprintf("h%s.csv", key)
	crtcsv := fmt.Sprintf("c%s.csv", key)
	totalhis := defaultKey(hiscsv, "0", totalmap)
	totalcrt := defaultKey(crtcsv, "0", totalmap)
	lines = append(lines, []string{totalhis, totalcrt, totalcrt, "0"})
	return lines
}
