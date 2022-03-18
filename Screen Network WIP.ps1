Function ExtractValidIPAddress($String){
    $IPregex=‘(?<Address>((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))’
    If ($String -Match $IPregex) {$Matches.Address}
}

$IPArray = @()
$ResultsArray = @()
$netDevices = @()
$getIPAddresses = arp.exe -a | Select-String "$Subnet.*dynamic" | select -Unique 
$getNetDevices = Get-NetNeighbor -AddressFamily IPv4 | Where-Object {($_.IPAddress -Like "192.168.1.*") -and ($_.State -notmatch "Unreachable")} | select LinkLayerAddress

ForEach ($IP in $getIPAddresses) {
    $IPArray += ExtractValidIPAddress $IP
}

#find a way to feed IP array into get net devices.

ForEach ($netdevice in $getNetDevices){
$netDevices += $getNetDevices.LinkLayerAddress
}

$netdevices = $netDevices | select -Unique

ForEach ($Mac in $netDevices) {
  If ($getNetDevices.LinkLayerAddress -contains $Mac) {
        $VarIP = ($getNetDevices | Where {$_.LinkLayerAddress -eq $Mac}).IPAddress
        $VarIP = $VarIP | select -Unique
        If ($VarIP.Count -eq 1) {
            Try {$DNSEntry = [System.Net.DNS]::GetHostEntry("$VarIP").HostName}
            Catch {$DNSEntry = "Unknown/Not Found"}
            $InfoObject = New-Object PsObject
            $InfoObject | Add-Member -MemberType NoteProperty -Name "MAC Address" -Value $Mac
            $InfoObject | Add-Member -MemberType NoteProperty -Name "IP Address" -Value $VarIP
            $InfoObject | Add-Member -MemberType NoteProperty -Name "Hostname" -Value $DNSEntry
            $ResultsArray += $InfoObject
        }
        Else {Write-Warning "$Mac will be skipped as more than one IP address was found in the ARP cache"}
    }
    Else {Write-Warning "$Mac will be skipped as there is no entry for it in the ARP cache"}
}
$ResultsArray