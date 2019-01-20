"""

"""

LoadEventNexus(Filename='/SNS/CNCS/IPTS-21344/nexus/CNCS_277537.nxs.h5', OutputWorkspace='CNCS_277537', LoadMonitors=True)
#SumSpectra(InputWorkspace='CNCS_277537', OutputWorkspace='CNCS_277537_summed')
#Rebin(InputWorkspace='CNCS_277537_summed', OutputWorkspace='CNCS_277537_summed', Params='10')

Rebin(InputWorkspace='CNCS_277537', OutputWorkspace='CNCS_277537_nxs_Rebin', Params='49500, 1000, 50500', PreserveEvents=False)

#mask out undesired regions of the detector array
MaskBTP(Workspace = 'CNCS_277537_nxs_Rebin', Instrument = 'CNCS', Bank = '35-39')
MaskBTP(Workspace = 'CNCS_277537_nxs_Rebin', Instrument = 'CNCS', Pixel = '121-128')
MaskBTP(Workspace = 'CNCS_277537_nxs_Rebin', Instrument = 'CNCS', Pixel = '1-8')

intensity_array = mtd['CNCS_277537_nxs_Rebin'].extractY()
intensity_mean = float(intensity_array[intensity_array>0].mean())
CreateSingleValuedWorkspace(OutputWorkspace='intensity_mean_ws',DataValue=intensity_mean)
Divide(LHSWorkspace='CNCS_277537_nxs_Rebin',RHSWorkspace='intensity_mean_ws',OutputWorkspace='normalized_vanadium') #Divide the vanadium by the mean
#Multiply(LHSWorkspace='reduce',RHSWorkspace='__meanval',OutputWorkspace='reduce') #multiple by the mean of vanadium Normalized data = Data / (Van/meanvan) = Data *meanvan/Van


SaveNexus(InputWorkspace="normalized_vanadium", Filename= '/SNS/CNCS/IPTS-20360/shared/vanadium_files/custom_processed_van_277537.nxs') 

normalized_vanadium_intensity_array = mtd['normalized_vanadium'].extractY()
normalized_vanadium_intensity_mean = float(intensity_array[intensity_array>0].mean())

print(intensity_mean)
print(normalized_vanadium_intensity_mean)

"""
    if DGSdict.has_key('SaveProcessedDetVan') and NormalizedVanadiumEqualToOne:
        filename=DGSdict['SaveProcDetVanFilename']
        change_permissions(filename,0664)
        LoadNexus(Filename=filename,OutputWorkspace="__VAN")
        datay = mtd['__VAN'].extractY()
        meanval = float(datay[datay>0].mean())
        CreateSingleValuedWorkspace(OutputWorkspace='__meanval',DataValue=meanval)
        Divide(LHSWorkspace='__VAN',RHSWorkspace='__meanval',OutputWorkspace='__VAN') #Divide the vanadium by the mean
        Multiply(LHSWorkspace='reduce',RHSWorkspace='__meanval',OutputWorkspace='reduce') #multiple by the mean of vanadium Normalized data = Data / (Van/meanvan) = Data *meanvan/Van
        SaveNexus(InputWorkspace="__VAN", Filename= filename) 
        change_permissions(filename,0664)
"""

LoadEventNexus(Filename='/SNS/CNCS/IPTS-21344/nexus/CNCS_277537.nxs.h5', OutputWorkspace='CNCS_277537', LoadMonitors=True)
MaskBTP(Workspace='CNCS_277537', Instrument='CNCS', Bank='35-39', MaskedDetectors='34816-39935')
MaskBTP(Workspace='CNCS_277537', Instrument='CNCS', Pixel='121-128', MaskedDetectors='120-127,248-255,376-383,504-511,632-639,760-767,888-895,1016-1023,1144-1151,1272-1279,1400-1407,1528-1535,1656-1663,1784-1791,1912-1919,2040-2047,2168-2175,2296-2303,2424-2431,2552-2559,2680-2687,2808-2815,2936-2943,3064-3071,3192-3199,3320-3327,3448-3455,3576-3583,3704-3711,3832-3839,3960-3967,4088-4095,4216-4223,4344-4351,4472-4479,4600-4607,4728-4735,4856-4863,4984-4991,5112-5119,5240-5247,5368-5375,5496-5503,5624-5631,5752-5759,5880-5887,6008-6015,6136-6143,6264-6271,6392-6399,6520-6527,6648-6655,6776-6783,6904-6911,7032-7039,7160-7167,7288-7295,7416-7423,7544-7551,7672-7679,7800-7807,7928-7935,8056-8063,8184-8191,8312-8319,8440-8447,8568-8575,8696-8703,8824-8831,8952-8959,9080-9087,9208-9215,9336-9343,9464-9471,9592-9599,9720-9727,9848-9855,9976-9983,10104-10111,10232-10239,10360-10367,10488-10495,10616-10623,10744-10751,10872-10879,11000-11007,11128-11135,11256-11263,11384-11391,11512-11519,11640-11647,11768-11775,11896-11903,12024-12031,12152-12159,12280-12287,12408-12415,12536-12543,12664-12671,12792-12799,12920-12927,13048-13055,13176-13183,13304-13311,13432-13439,13560-13567,13688-13695,13816-13823,13944-13951,14072-14079,14200-14207,14328-14335,14456-14463,14584-14591,14712-14719,14840-14847,14968-14975,15096-15103,15224-15231,15352-15359,15480-15487,15608-15615,15736-15743,15864-15871,15992-15999,16120-16127,16248-16255,16376-16383,16504-16511,16632-16639,16760-16767,16888-16895,17016-17023,17144-17151,17272-17279,17400-17407,17528-17535,17656-17663,17784-17791,17912-17919,18040-18047,18168-18175,18296-18303,18424-18431,18552-18559,18680-18687,18808-18815,18936-18943,19064-19071,19192-19199,19320-19327,19448-19455,19576-19583,19704-19711,19832-19839,19960-19967,20088-20095,20216-20223,20344-20351,20472-20479,20600-20607,20728-20735,20856-20863,20984-20991,21112-21119,21240-21247,21368-21375,21496-21503,21624-21631,21752-21759,21880-21887,22008-22015,22136-22143,22264-22271,22392-22399,22520-22527,22648-22655,22776-22783,22904-22911,23032-23039,23160-23167,23288-23295,23416-23423,23544-23551,23672-23679,23800-23807,23928-23935,24056-24063,24184-24191,24312-24319,24440-24447,24568-24575,24696-24703,24824-24831,24952-24959,25080-25087,25208-25215,25336-25343,25464-25471,25592-25599,25720-25727,25848-25855,25976-25983,26104-26111,26232-26239,26360-26367,26488-26495,26616-26623,26744-26751,26872-26879,27000-27007,27128-27135,27256-27263,27384-27391,27512-27519,27640-27647,27768-27775,27896-27903,28024-28031,28152-28159,28280-28287,28408-28415,28536-28543,28664-28671,28792-28799,28920-28927,29048-29055,29176-29183,29304-29311,29432-29439,29560-29567,29688-29695,29816-29823,29944-29951,30072-30079,30200-30207,30328-30335,30456-30463,30584-30591,30712-30719,30840-30847,30968-30975,31096-31103,31224-31231,31352-31359,31480-31487,31608-31615,31736-31743,31864-31871,31992-31999,32120-32127,32248-32255,32376-32383,32504-32511,32632-32639,32760-32767,32888-32895,33016-33023,33144-33151,33272-33279,33400-33407,33528-33535,33656-33663,33784-33791,33912-33919,34040-34047,34168-34175,34296-34303,34424-34431,34552-34559,34680-34687,34808-34815,34936-34943,35064-35071,35192-35199,35320-35327,35448-35455,35576-35583,35704-35711,35832-35839,35960-35967,36088-36095,36216-36223,36344-36351,36472-36479,36600-36607,36728-36735,36856-36863,36984-36991,37112-37119,37240-37247,37368-37375,37496-37503,37624-37631,37752-37759,37880-37887,38008-38015,38136-38143,38264-38271,38392-38399,38520-38527,38648-38655,38776-38783,38904-38911,39032-39039,39160-39167,39288-39295,39416-39423,39544-39551,39672-39679,39800-39807,39928-39935,40056-40063,40184-40191,40312-40319,40440-40447,40568-40575,40696-40703,40824-40831,40952-40959,41080-41087,41208-41215,41336-41343,41464-41471,41592-41599,41720-41727,41848-41855,41976-41983,42104-42111,42232-42239,42360-42367,42488-42495,42616-42623,42744-42751,42872-42879,43000-43007,43128-43135,43256-43263,43384-43391,43512-43519,43640-43647,43768-43775,43896-43903,44024-44031,44152-44159,44280-44287,44408-44415,44536-44543,44664-44671,44792-44799,44920-44927,45048-45055,45176-45183,45304-45311,45432-45439,45560-45567,45688-45695,45816-45823,45944-45951,46072-46079,46200-46207,46328-46335,46456-46463,46584-46591,46712-46719,46840-46847,46968-46975,47096-47103,47224-47231,47352-47359,47480-47487,47608-47615,47736-47743,47864-47871,47992-47999,48120-48127,48248-48255,48376-48383,48504-48511,48632-48639,48760-48767,48888-48895,49016-49023,49144-49151,49272-49279,49400-49407,49528-49535,49656-49663,49784-49791,49912-49919,50040-50047,50168-50175,50296-50303,50424-50431,50552-50559,50680-50687,50808-50815,50936-50943,51064-51071,51192-51199')
MaskBTP(Workspace='CNCS_277537', Instrument='CNCS', Pixel='1-8', MaskedDetectors='0-7,128-135,256-263,384-391,512-519,640-647,768-775,896-903,1024-1031,1152-1159,1280-1287,1408-1415,1536-1543,1664-1671,1792-1799,1920-1927,2048-2055,2176-2183,2304-2311,2432-2439,2560-2567,2688-2695,2816-2823,2944-2951,3072-3079,3200-3207,3328-3335,3456-3463,3584-3591,3712-3719,3840-3847,3968-3975,4096-4103,4224-4231,4352-4359,4480-4487,4608-4615,4736-4743,4864-4871,4992-4999,5120-5127,5248-5255,5376-5383,5504-5511,5632-5639,5760-5767,5888-5895,6016-6023,6144-6151,6272-6279,6400-6407,6528-6535,6656-6663,6784-6791,6912-6919,7040-7047,7168-7175,7296-7303,7424-7431,7552-7559,7680-7687,7808-7815,7936-7943,8064-8071,8192-8199,8320-8327,8448-8455,8576-8583,8704-8711,8832-8839,8960-8967,9088-9095,9216-9223,9344-9351,9472-9479,9600-9607,9728-9735,9856-9863,9984-9991,10112-10119,10240-10247,10368-10375,10496-10503,10624-10631,10752-10759,10880-10887,11008-11015,11136-11143,11264-11271,11392-11399,11520-11527,11648-11655,11776-11783,11904-11911,12032-12039,12160-12167,12288-12295,12416-12423,12544-12551,12672-12679,12800-12807,12928-12935,13056-13063,13184-13191,13312-13319,13440-13447,13568-13575,13696-13703,13824-13831,13952-13959,14080-14087,14208-14215,14336-14343,14464-14471,14592-14599,14720-14727,14848-14855,14976-14983,15104-15111,15232-15239,15360-15367,15488-15495,15616-15623,15744-15751,15872-15879,16000-16007,16128-16135,16256-16263,16384-16391,16512-16519,16640-16647,16768-16775,16896-16903,17024-17031,17152-17159,17280-17287,17408-17415,17536-17543,17664-17671,17792-17799,17920-17927,18048-18055,18176-18183,18304-18311,18432-18439,18560-18567,18688-18695,18816-18823,18944-18951,19072-19079,19200-19207,19328-19335,19456-19463,19584-19591,19712-19719,19840-19847,19968-19975,20096-20103,20224-20231,20352-20359,20480-20487,20608-20615,20736-20743,20864-20871,20992-20999,21120-21127,21248-21255,21376-21383,21504-21511,21632-21639,21760-21767,21888-21895,22016-22023,22144-22151,22272-22279,22400-22407,22528-22535,22656-22663,22784-22791,22912-22919,23040-23047,23168-23175,23296-23303,23424-23431,23552-23559,23680-23687,23808-23815,23936-23943,24064-24071,24192-24199,24320-24327,24448-24455,24576-24583,24704-24711,24832-24839,24960-24967,25088-25095,25216-25223,25344-25351,25472-25479,25600-25607,25728-25735,25856-25863,25984-25991,26112-26119,26240-26247,26368-26375,26496-26503,26624-26631,26752-26759,26880-26887,27008-27015,27136-27143,27264-27271,27392-27399,27520-27527,27648-27655,27776-27783,27904-27911,28032-28039,28160-28167,28288-28295,28416-28423,28544-28551,28672-28679,28800-28807,28928-28935,29056-29063,29184-29191,29312-29319,29440-29447,29568-29575,29696-29703,29824-29831,29952-29959,30080-30087,30208-30215,30336-30343,30464-30471,30592-30599,30720-30727,30848-30855,30976-30983,31104-31111,31232-31239,31360-31367,31488-31495,31616-31623,31744-31751,31872-31879,32000-32007,32128-32135,32256-32263,32384-32391,32512-32519,32640-32647,32768-32775,32896-32903,33024-33031,33152-33159,33280-33287,33408-33415,33536-33543,33664-33671,33792-33799,33920-33927,34048-34055,34176-34183,34304-34311,34432-34439,34560-34567,34688-34695,34816-34823,34944-34951,35072-35079,35200-35207,35328-35335,35456-35463,35584-35591,35712-35719,35840-35847,35968-35975,36096-36103,36224-36231,36352-36359,36480-36487,36608-36615,36736-36743,36864-36871,36992-36999,37120-37127,37248-37255,37376-37383,37504-37511,37632-37639,37760-37767,37888-37895,38016-38023,38144-38151,38272-38279,38400-38407,38528-38535,38656-38663,38784-38791,38912-38919,39040-39047,39168-39175,39296-39303,39424-39431,39552-39559,39680-39687,39808-39815,39936-39943,40064-40071,40192-40199,40320-40327,40448-40455,40576-40583,40704-40711,40832-40839,40960-40967,41088-41095,41216-41223,41344-41351,41472-41479,41600-41607,41728-41735,41856-41863,41984-41991,42112-42119,42240-42247,42368-42375,42496-42503,42624-42631,42752-42759,42880-42887,43008-43015,43136-43143,43264-43271,43392-43399,43520-43527,43648-43655,43776-43783,43904-43911,44032-44039,44160-44167,44288-44295,44416-44423,44544-44551,44672-44679,44800-44807,44928-44935,45056-45063,45184-45191,45312-45319,45440-45447,45568-45575,45696-45703,45824-45831,45952-45959,46080-46087,46208-46215,46336-46343,46464-46471,46592-46599,46720-46727,46848-46855,46976-46983,47104-47111,47232-47239,47360-47367,47488-47495,47616-47623,47744-47751,47872-47879,48000-48007,48128-48135,48256-48263,48384-48391,48512-48519,48640-48647,48768-48775,48896-48903,49024-49031,49152-49159,49280-49287,49408-49415,49536-49543,49664-49671,49792-49799,49920-49927,50048-50055,50176-50183,50304-50311,50432-50439,50560-50567,50688-50695,50816-50823,50944-50951,51072-51079')

