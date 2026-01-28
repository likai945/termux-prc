// Dec 1, 2024
// Jul 25, 2025
// Jul 30, 2025
// Jan 23, 2026 no need to unzip manually
// by LiKai

package main

import (
	"bufio"
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
	"time"

	"github.com/dablelv/cyan/zip"
	"github.com/xuri/excelize/v2"
)

var (
	f                = excelize.NewFile()
	smrr, hisr, crtr int
	totalmap                = map[string]string{}
	currentTime             = getTime()
	date             string = currentTime.Format("2006-01-02")
	namedate         string = currentTime.Format("20060102")
	bookname         string = fmt.Sprintf("附件3：告警分析-中兴资源池-%s.xlsx", namedate)
	pools                   = []string{"可信3", "可信4", "可信5", "DMZ9", "可信11", "可信14", "DMZ16", "可信17"}
	timedict                = map[string]string{}
	timefill         string = "auto"
	styletype        string = "format"
)

func main() {
	before()
	if fileExist("config") {
		pools = readFile("config")[0]
	}
	for _, pool := range pools {
		re := regexp.MustCompile("[0-9]+")
		nums := re.FindAllString(pool, -1)
		cfile := fmt.Sprintf("c%s.zip", nums[0])
		hfile := fmt.Sprintf("h%s.zip", nums[0])
		writeSheet("Sheet2", pool, hisr, checkExist(hfile, pool, 4))
		writeSheet("Sheet3", pool, crtr, checkExist(cfile, pool, 3))
		writeSheet("Sheet1", pool, smrr, getKey(nums[0]))
	}
	after()
}

func getTime() time.Time {
	ctime := time.Now()
	cstSh, err := time.LoadLocation("Asia/Shanghai")
	if err == nil {
		ctime = ctime.In(cstSh)
	}
	return ctime
}

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
	for _, prerow := range alrmsli {
		row := removeRocks(prerow) // fp
		desc := row[indx]
		rowval := amap[desc]
		sttt := append(rowval[0], row[7])
		et := defaultKey(file, row[9], timedict)
		endt := append(rowval[1], et)
		devi := append(rowval[2], row[5]+"名="+row[6])
		amap[desc] = [3][]string{sttt, endt, devi}
	}
	return amap
}

func removeRocks(prerow []string) []string {
	var row []string
	for _, item := range prerow {
		if item != "admin" {
			row = append(row, item)
		}
	}
	return row
} // fp

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

	smrtitle := []string{"时间", "资源池", "历史告警数量", "当前告警数量", "当前告警清除数量", "当前告警剩余"}
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
		4: {{"无告警，不涉及", "无告警，不涉及", "无告警，不涉及", "无告警，不涉及", "0", "无告警，不涉及"}},
		3: {{"无告警，不涉及", "无告警，不涉及", "无告警，不涉及", "无告警，不涉及", "0", "无告警，不涉及", "是"}},
	}
	hcchmap := map[int]string{4: "历史", 3: "当前"}
	// magic num 4 is his, 3 is crt
	fexist, _ := filepath.Glob(file)
	var command string
	if fileExist("config") {
		timefill = readFile("config")[2][0]
	}
	if len(fexist) == 0 {
		fmt.Printf("\033[32m%s\033[0m不存在,若\033[32m%s\033[0m无\033[32m%s\033[0m告警，请输入OK，否则输入NG以退出。\n", file, pool, hcchmap[hc])
		fmt.Scanln(&command)
		if strings.EqualFold(command, "OK") {
			return hcmap[hc]
		} else {
			rmFiles()
			os.Exit(2)
		}
	}

	unzfile := unzip(file)

	if hc == 3 && timefill == "auto" {
		timedict[unzfile] = currentTime.Format("2006-01-02 03:04:05")
	} else if hc == 3 && timefill == "no" {
		fmt.Printf("%s当前告警清除时间：", pool)
		reader := bufio.NewReader(os.Stdin)
		pdeltime, _ := reader.ReadString('\n')
		deltime := strings.TrimRight(pdeltime, "\n")
		timedict[unzfile] = deltime
	}
	return toWall(unzfile, hc)
}

func toDict() map[string]string {
	var resarr [][]string
	amap := map[string]string{}
	if fileExist("result.csv") {
		resarr = readFile("result.csv")
	} else {
		return amap
	}
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

	if fileExist("config") {
		styletype = readFile("config")[4][0]
	}
	if styletype == "format" {
		style()
	} else {
		styless()
	}

	f.SetSheetName("Sheet1", "汇总")
	f.SetSheetName("Sheet2", "历史告警处理记录")
	f.SetSheetName("Sheet3", "当前告警处理记录")

	f.SaveAs(bookname)
	mvFiles()
}

func style() {
	styleIdnc, _ := f.NewStyle(&excelize.Style{
		Border: []excelize.Border{
			{Type: "left", Color: "000000", Style: 1},
			{Type: "top", Color: "000000", Style: 1},
			{Type: "bottom", Color: "000000", Style: 1},
			{Type: "right", Color: "000000", Style: 1},
		},
		Alignment: &excelize.Alignment{
			Vertical: "center",
			WrapText: true,
		},
		Font: &excelize.Font{
			Family: "宋体",
		},
	})
	styleIdc, _ := f.NewStyle(&excelize.Style{
		Border: []excelize.Border{
			{Type: "left", Color: "000000", Style: 1},
			{Type: "top", Color: "000000", Style: 1},
			{Type: "bottom", Color: "000000", Style: 1},
			{Type: "right", Color: "000000", Style: 1},
		},
		Alignment: &excelize.Alignment{
			Horizontal: "center",
			Vertical:   "center",
			WrapText:   true,
		},
		Font: &excelize.Font{
			Family: "宋体",
		},
	})

	sfar := fmt.Sprintf("F%d", smrr)
	hfar := fmt.Sprintf("H%d", hisr+1)
	cfar := fmt.Sprintf("J%d", crtr+1)
	chcolfar := fmt.Sprintf("H%d", crtr+1)
	hcent := fmt.Sprintf("D%d", hisr+1)
	ccent := fmt.Sprintf("D%d", crtr+1)
	hcl := fmt.Sprintf("G%d", hisr+1)
	ccl := fmt.Sprintf("I%d", crtr+1)
	f.SetCellStyle("Sheet1", "A1", sfar, styleIdc)

	f.SetCellStyle("Sheet2", "E1", hfar, styleIdnc)
	f.SetCellStyle("Sheet2", "A3", hcent, styleIdc)
	f.SetCellStyle("Sheet2", "G3", hcl, styleIdc)
	f.SetCellStyle("Sheet2", "A1", "H2", styleIdc)

	f.SetCellStyle("Sheet3", "E1", cfar, styleIdnc)
	f.SetCellStyle("Sheet3", "A3", ccent, styleIdc)
	f.SetCellStyle("Sheet3", "G3", ccl, styleIdc)
	f.SetCellStyle("Sheet3", "A1", "J2", styleIdc)
	f.SetCellStyle("Sheet3", "H1", chcolfar, styleIdnc)

	smwdth := map[string]float64{"A": 11, "B": 7, "C": 13, "D": 13, "E": 17, "F": 13}
	hcwdth := map[string]float64{"A": 11, "B": 8, "C": 20, "D": 20, "E": 45, "F": 22, "G": 10, "H": 22, "I": 10, "J": 17}
	for col, wdth := range smwdth {
		f.SetColWidth("Sheet1", col, col, wdth)
	}
	for col, wdth := range hcwdth {
		f.SetColWidth("Sheet2", col, col, wdth)
		f.SetColWidth("Sheet3", col, col, wdth)
	}
}

func styless() {
	styleIdc, _ := f.NewStyle(&excelize.Style{
		Alignment: &excelize.Alignment{
			Horizontal: "center",
		},
	})

	f.SetCellStyle("Sheet2", "A1", "A1", styleIdc)
	f.SetCellStyle("Sheet3", "A1", "A1", styleIdc)
}

func defaultKey(key, defval string, anymap map[string]string) string {
	_, exist := anymap[key]
	if exist {
		return anymap[key]
	} else {
		return defval
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

func fileExist(fl string) bool {
	if _, err := os.Stat(fl); err == nil {
		return true
	} else {
		return false
	}
}

func mvFile(file string) {
	dirname := fmt.Sprintf("done-%s", namedate)
	os.Mkdir(dirname, 0o755)
	newpath := fmt.Sprintf("%s/%s", dirname, file)
	if fileExist(file) {
		os.Rename(file, newpath)
	}
}

func mvFiles() {
	for _, pool := range pools {
		re := regexp.MustCompile("[0-9]+")
		nums := re.FindAllString(pool, -1)
		cfile := fmt.Sprintf("c%s.csv", nums[0])
		mvFile(cfile)
		czipfile := fmt.Sprintf("c%s.zip", nums[0])
		mvFile(czipfile)
		hfile := fmt.Sprintf("h%s.csv", nums[0])
		mvFile(hfile)
		hzipfile := fmt.Sprintf("h%s.zip", nums[0])
		mvFile(hzipfile)
	}
}

func rmFile(file string) {
	if fileExist(file) {
		os.Remove(file)
	}
}

func rmFiles() {
	for _, pool := range pools {
		re := regexp.MustCompile("[0-9]+")
		nums := re.FindAllString(pool, -1)
		cfile := fmt.Sprintf("c%s.csv", nums[0])
		rmFile(cfile)
		hfile := fmt.Sprintf("h%s.csv", nums[0])
		rmFile(hfile)
	}
}

func unzip(zipname string) string {
	dirname := strings.Replace(zipname, ".zip", "", -1)
	patn := dirname + "/*/*.csv"
	csvname := dirname + ".csv"
	_ = zip.Unzip(zipname, dirname)
	file, _ := filepath.Glob(patn)
	_ = os.Rename(file[0], csvname)
	_ = os.RemoveAll(dirname)
	return csvname
}
