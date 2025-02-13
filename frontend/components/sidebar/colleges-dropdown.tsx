"use client";
import {
  Dropdown,
  DropdownItem,
  DropdownMenu,
  DropdownSection,
  DropdownTrigger,
} from "@nextui-org/react";
import React, { useState } from "react";
import { AcmeIcon } from "../icons/acme-icon";
import { AcmeLogo } from "../icons/acmelogo";
import { BottomIcon } from "../icons/sidebar/bottom-icon";

interface College {
  name: string;
  location: string;
  logo: React.ReactNode;
}

export const CollegesDropdown = () => {
  const [college, setCollege] = useState<College>({
    name: "Grays Harbor College",
    location: "Aberdeen, WA",
    logo: <AcmeIcon />,
  });

  return (
    <Dropdown classNames={{ base: "w-full min-w-[320px]" }}>
      <DropdownTrigger className="cursor-pointer">
        <div className="flex items-center gap-2">
          {college.logo}
          <div className="flex flex-col gap-1">
            <h3 className="text-xl font-medium m-0 text-default-900">
              {college.name}
            </h3>
            <span className="text-xs font-medium text-default-500">
              {college.location}
            </span>
          </div>
          <BottomIcon />
        </div>
      </DropdownTrigger>
      <DropdownMenu
        onAction={(key) => {
          if (key === "1") {
            setCollege({
              name: "Grays Harbor College",
              location: "Aberdeen, WA",
              logo: <AcmeIcon />,
            });
          }
          if (key === "2") {
            setCollege({
              name: "Olympic College",
              location: "Bremerton, WA",
              logo: <AcmeLogo />,
            });
          }
          if (key === "3") {
            setCollege({
              name: "Seattle Central College",
              location: "Seattle, WA",
              logo: <AcmeIcon />,
            });
          }
          if (key === "4") {
            setCollege({
              name: "Tacoma Community College",
              location: "Tacoma, WA",
              logo: <AcmeIcon />,
            });
          }
        }}
        aria-label="College Selection"
      >
        <DropdownSection title="Colleges">
          <DropdownItem
            key="1"
            startContent={<AcmeIcon />}
            description="Aberdeen, WA"
            classNames={{
              base: "py-4",
              title: "text-base font-semibold",
            }}
          >
            Grays Harbor College
          </DropdownItem>
          <DropdownItem
            key="2"
            startContent={<AcmeLogo />}
            description="Bremerton, WA"
            classNames={{
              base: "py-4",
              title: "text-base font-semibold",
            }}
          >
            Olympic College
          </DropdownItem>
          <DropdownItem
            key="3"
            startContent={<AcmeIcon />}
            description="Seattle, WA"
            classNames={{
              base: "py-4",
              title: "text-base font-semibold",
            }}
          >
            Seattle Central College
          </DropdownItem>
          <DropdownItem
            key="4"
            startContent={<AcmeIcon />}
            description="Tacoma, WA"
            classNames={{
              base: "py-4",
              title: "text-base font-semibold",
            }}
          >
            Tacoma Community College
          </DropdownItem>
        </DropdownSection>
      </DropdownMenu>
    </Dropdown>
  );
};
