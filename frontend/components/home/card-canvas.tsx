import { Card, CardBody } from "@nextui-org/react";
import React from "react";
import { CanvasLogo } from "../logos/canvaslogo";

export const CanvasCard = () => {
  return (
    <a
      href="https://canvas.instructure.com"
      target="_blank"
      rel="noopener noreferrer"
      className="block"
    >
      <Card className="xl:max-w-sm bg-[#2E9AFE] rounded-xl shadow-md px-3 w-full hover:shadow-lg transition-shadow">
        <CardBody className="py-5 overflow-hidden">
          <div className="flex items-center gap-3">
            <CanvasLogo className="w-8 h-8" />
            <span className="text-white text-lg font-bold">Canvas LMS</span>
          </div>
          <div className="mt-3">
            <span className="text-white text-sm">
              Access your courses, grades, and assignments on Canvas.
            </span>
          </div>
        </CardBody>
      </Card>
    </a>
  );
};
