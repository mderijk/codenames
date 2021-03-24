<?php
$SERVER_DIRECTORY = '../server';
$SERVER_FILE = 'server.py';

// select correct path to python executable (the file structure of python virtual environments differs between operating systems)
if (strtoupper(substr(PHP_OS, 0, 3)) === 'WIN') $PYTHON_PATH = 'venv\Scripts\python'; # Windows
else $PYTHON_PATH = 'venv/bin/python'; # Linux

if (!empty($input = file_get_contents('php://input')))
{
	// try to launch the application
	$cmd = "$PYTHON_PATH $SERVER_FILE";
	$descriptorspec = array(
		0 => array('pipe', 'r'),
		1 => array('pipe', 'w'),
		2 => array('file',  "$SERVER_DIRECTORY/logs/php.log", 'a'),
	);
	$cwd = dirname(__FILE__) . "/$SERVER_DIRECTORY";
	$process = proc_open($cmd, $descriptorspec, $pipes, $cwd);
	
	if (is_resource($process))
	{
		fwrite($pipes[0], $input);
		fclose($pipes[0]);
		
		$json = stream_get_contents($pipes[1]);
		fclose($pipes[1]);
		proc_close($process);
	}
	else
	{
		$data = array(
			'error' => 'Failed to reach server',
			'status' => 'error',
		);
		$json = json_encode($data);
	}
}
else
{
	$data = array(
		'error' => 'No input',
		'status' => 'error',
	);
	$json = json_encode($data);
}

// Return JSON and exit
header('Content-Type: application/json');
echo $json;
